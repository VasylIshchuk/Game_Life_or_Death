from ..core.game_entity import GameEntity, load_data_from_file, initialize_general_attributes
from .limits_stats import LimitsStats

import random

MAX_ATTACK_POINTS = 60


def _generate_random_value(min_value, max_value):
    return random.randint(min_value, max_value)


class Creature(GameEntity):
    """Represents a game creature with combat-related attributes and methods."""

    def __init__(self, title):
        """Initializes a creature with attributes loaded from a data file."""
        super().__init__(title)
        self.type: str = ""
        self.category: str = ""
        self.icon: str = ""
        self.level: int = 0
        self.health_points: int = 0
        self.attack_power: int = 0
        self.defense: int = 0
        self.attack_range: int = 0
        self.agility: int = 0
        self.abilities: str = ""
        self.is_alive: bool = True

        self.HIT_CHANCE = 0.0  # Used for testing hit probability
        self.data_creature = load_data_from_file("./creatures.json", title)

        initialize_general_attributes(self, self.data_creature)
        self._initialize_generated_attributes()
        self.max_health_points = self.health_points

    def _initialize_generated_attributes(self):
        """Initializes health, defense, and agility stats from limits or reserved values."""
        stats = LimitsStats.get_stats(self.category)
        if stats:
            self.health_points = _generate_random_value(*stats["health_points"])
            self.defense = _generate_random_value(*stats["defense"])
            self.agility = _generate_random_value(*stats["agility"])

    def check_is_alive(self):
        """Update the creature's alive status based on its health."""
        if self.health_points <= 0:
            self.is_alive = False

    def healing(self, points):
        """Heals the creature by the given number of points."""
        if self.health_points + points >= self.max_health_points:
            self.health_points = self.max_health_points
        else:
            self.health_points += points

    def is_within_range(self, enemy, range_radius):
        """Check if an enemy is within a square range of the creature."""
        return (
                self.position.x - range_radius <= enemy.position.x <= self.position.x + range_radius and
                self.position.y - range_radius <= enemy.position.y <= self.position.y + range_radius
        )

    def attack(self, enemy):
        """Perform an attack on an enemy and calculate its result."""
        self.luck = self._roll_dice()

        hit_probability = self._calculate_hit_probability(self.attack_power, enemy)

        if self._check_attack_hit(hit_probability):
            self._apply_damage_to_enemy(enemy, self.attack_power)
            return True
        return False

    def _roll_dice(self):
        return random.randint(1, 20)

    def _calculate_hit_probability(self, attack_power, enemy):
        """Calculate the probability of a successful hit on the enemy."""
        attack_points = self._calculate_attack_points(attack_power)
        defense_points = self._calculate_defense_points(enemy)

        hit_probability = (attack_points - defense_points + MAX_ATTACK_POINTS) / (2 * MAX_ATTACK_POINTS)
        hit_probability = self._clamp_chance(hit_probability)
        self.HIT_CHANCE = hit_probability
        return hit_probability

    def _calculate_attack_points(self, attack_power):
        return self.luck + self.level + attack_power

    def _calculate_defense_points(self, enemy):
        return enemy.level + enemy.agility

    def _check_attack_hit(self, hit_probability):
        """Calculate the probability of a successful hit on the enemy."""
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
        """Applies damage to the target considering its defense."""
        if enemy.defense > 0:
            if enemy.defense >= attack:
                enemy.defense -= attack
            else:
                enemy.health_points -= attack - enemy.defense
                enemy.defense = 0
        elif enemy.health_points > attack:
            enemy.health_points -= attack
        else:
            enemy.health_points = 0
            enemy.check_is_alive()

    def _clamp_chance(self, efficiency_chance):
        """Clamps the hit chance to a minimum of 20% and a maximum of 90%."""
        if efficiency_chance > 0.9:
            return 0.9
        elif efficiency_chance < 0.2:
            return 0.2
        else:
            return efficiency_chance
