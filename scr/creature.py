from game_entity import GameEntity, _load_data_from_file, _parse_attribute
from limits_stats import LimitsStats
from weapon import Weapon

import random

MAX_ATTACK_POINTS = 50


def _generate_random_value(min_value, max_value):
    return random.randint(min_value, max_value)


class Creature(GameEntity):

    def __init__(self, title):
        """Initializes a creature with attributes loaded from a data file."""
        super().__init__(title)
        self.health_points = None
        self.category = None
        self.type = None
        self.level = None
        self.attack_power = None
        self.is_alive = True

        self.HIT_CHANCE = 0.0  # only need for test
        self.data_creatures = _load_data_from_file("../creatures.json", title)

        attributes = ["type", "category", "icon", "description", "level", "skills", "attack_power", "attack_range"]
        self._initialize_general_attributes(attributes)
        self._initialize_stats()
        self.max_health_points = self.health_points
        self._initialize_optional_attribute()

    def _initialize_general_attributes(self, attributes):
        """Initialize general attributes shared by all creatures."""
        for attr in attributes:
            setattr(self, attr, self._get_attribute(attr))

    def _initialize_optional_attribute(self):
        """Initialize optional attributes"""
        weapon = _parse_attribute(self.data_creatures, "weapon")
        self.weapon = Weapon(weapon) if weapon is not None else None

    def _get_attribute(self, attribute_name):
        """Retrieves an attribute value from the loaded data."""
        return _parse_attribute(self.data_creatures, attribute_name)

    def _initialize_stats(self):
        """Initializes health, defense, and agility stats from limits or reserved values."""
        stats = LimitsStats.get_stats(self.category)
        if stats:
            self.health_points = _generate_random_value(*stats["health_points"])
            self.defense = _generate_random_value(*stats["defense"])
            self.agility = _generate_random_value(*stats["agility"])
        else:
            self.health_points = int(self._get_attribute("health_points") or 0)
            self.defense = int(self._get_attribute("defense") or 0)
            self.agility = int(self._get_attribute("agility") or 0)

    def check_is_alive(self):
        if self.health_points <= 0:
            self.is_alive = False

    def healing(self, points):
        """Heals the creature by the given number of points."""
        if self.health_points + points >= self.max_health_points:
            self.health_points = self.max_health_points
        else:
            self.health_points += points

    def attack(self, enemy):
        """Calculates and applies the result of an attack."""

        result_dice = random.randint(1, 20)

        efficiency_chance = self.calculate_hit_chance(enemy, self.attack_power, result_dice)
        random_factor = random.random()

        if result_dice == 20 or (result_dice != 1 and random_factor <= efficiency_chance):
            self._apply_damage_to_enemy(enemy, self.attack_power)
            return True
        return False

    def calculate_hit_chance(self, enemy, attack, result_dice):
        """Calculates the chance to successfully hit the target."""
        attack_points = result_dice + self.level + attack
        defense_points = enemy.level + enemy.agility

        efficiency_chance = (attack_points - defense_points + MAX_ATTACK_POINTS) / (2 * MAX_ATTACK_POINTS)
        self.HIT_CHANCE = efficiency_chance
        return self._clamp_chance(efficiency_chance)

    def _clamp_chance(self, efficiency_chance):
        """Clamps the hit chance to a minimum of 10% and a maximum of 90%."""
        if efficiency_chance > 0.9:
            return 0.9
        elif efficiency_chance < 0.1:
            return 0.1
        else:
            return efficiency_chance

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
            enemy.is_alive = False
