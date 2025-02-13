import random

from ..core.game_entity import GameEntity, initialize_attributes_from_data
from ..core.data_loader import load_entity_data_from_file
from .limits_stats import LimitsAttributes

MAX_ATTACK_POINTS = 60


def _generate_random_value(min_value, max_value):
    return random.randint(min_value, max_value)


class Creature(GameEntity):

    def __init__(self, title):
        super().__init__(title)
        self.type: str = ""
        self.level: int = 0
        self.health_points: int = 0
        self.attack_power: int = 0
        self.defense: int = 0
        self.attack_range: int = 0
        self.agility: int = 0
        self.abilities: str = ""
        self.is_alive: bool = True

        self.HIT_CHANCE = 0.0  # Used for testing hit probability
        self.data_creature = load_entity_data_from_file("./creatures.json", title)

        initialize_attributes_from_data(self, self.data_creature)
        self._initialize_generated_attributes()
        self.max_health_points = self.health_points

    def _initialize_generated_attributes(self):
        attributes = LimitsAttributes.get_attributes(self.category)
        if attributes:
            self.health_points = _generate_random_value(*attributes["health_points"])
            self.defense = _generate_random_value(*attributes["defense"])
            self.agility = _generate_random_value(*attributes["agility"])

    def get_attack_power(self):
        return self.attack_power

    def get_agility(self):
        return self.agility

    def get_defense(self):
        return self.defense

    def update_defense(self, value):
        self.defense = value

    def increase_attack_power(self, value):
        self.attack_power += value

    def set_is_dead(self):
        self.is_alive = False

    def decrease_health_points(self, points):
        if self.health_points - points <= 0:
            self.set_is_dead()
            self.health_points = 0
        else:
            self.health_points -= points

    def healing(self, points):
        if self.health_points + points >= self.max_health_points:
            self.health_points = self.max_health_points
        else:
            self.health_points += points

    def is_within_range(self, enemy, range_radius, game_map=None):
        if not self._is_on_same_area(game_map, enemy): return False
        return (
                self.get_x_position() - range_radius <= enemy.get_x_position() <= self.get_x_position() + range_radius and
                self.get_y_position() - range_radius <= enemy.get_y_position() <= self.get_y_position() + range_radius
        )

    def _is_on_same_area(self, game_map, enemy):
        creature_position = self.get_position()
        enemy_position = enemy.get_position()
        return (game_map is not None and
                game_map.get_cell_icon(creature_position) == game_map.get_cell_icon(enemy_position))

    def attack(self, enemy, game_map=None):
        self.luck = self._roll_dice()

        hit_probability = self._calculate_hit_probability(self.get_attack_power(), enemy)

        if self._is_hit_successful(hit_probability):
            self._apply_damage_to_enemy(enemy, self.get_attack_power())
            return True
        return False

    def _roll_dice(self):
        return random.randint(1, 20)

    def _calculate_hit_probability(self, attack_power, enemy):
        attack_points = self._calculate_attack_points(attack_power)
        defense_points = self._calculate_defense_points(enemy)

        hit_probability = (attack_points - defense_points + MAX_ATTACK_POINTS) / (2 * MAX_ATTACK_POINTS)
        hit_probability = self._clamp_chance(hit_probability)
        self.HIT_CHANCE = hit_probability
        return hit_probability

    def _calculate_attack_points(self, attack_power):
        return self.luck + self.level + attack_power

    def _calculate_defense_points(self, enemy):
        return enemy.level + enemy.get_agility()

    def _is_hit_successful(self, hit_probability):
        if self._is_critical_success() or (
                not self._is_critical_failure() and self._is_hit(hit_probability)):
            return True
        return False

    def _is_critical_success(self):
        return self.luck == 20

    def _is_critical_failure(self):
        return self.luck == 1

    def _is_hit(self, hit_probability):
        random_factor = random.random()
        return random_factor <= hit_probability

    def _apply_damage_to_enemy(self, enemy, attack):
        if enemy.get_defense() > 0:
            if enemy.get_defense() >= attack:
                new_defence = enemy.get_defense() - attack
                enemy.update_defense(new_defence)
            else:
                enemy.health_points -= attack - enemy.get_defense()
                enemy.update_defense(0)
        elif enemy.health_points > attack:
            enemy.health_points -= attack
        else:
            enemy.health_points = 0
            enemy.set_is_dead()

    def _clamp_chance(self, efficiency_chance):
        if efficiency_chance > 0.9:
            return 0.9
        elif efficiency_chance < 0.2:
            return 0.2
        else:
            return efficiency_chance
