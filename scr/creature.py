from game_entity import GameEntity, _load_data_from_file, _parse_attribute
from limits_stats import LimitsStats
from inventory import Inventory
from weapon import Weapon

import random

MAX_ATTACK_POINTS = 50

"""Applies damage to the target considering its defense."""
def _apply_damage_to_enemy(enemy, attack):
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


def _generate_random_value(min_value, max_value):
    return random.randint(min_value, max_value)


class Creature(GameEntity):

    """Initializes a creature with attributes loaded from a data file."""
    def __init__(self, title):
        super().__init__(title)
        self.HIT_CHANCE = 0.0  # only need for test
        self.data_creatures = _load_data_from_file("../creatures.json", title)

        self.is_alive = True
        self.attack_range_spirit_power = 2
        # Special handling for "Mark"
        if title == 'Mark':
            self.mental_state = _parse_attribute(self.data_creatures, "mental_state")
            self.inventory = Inventory()
        # General attributes
        self.category = self._get_attribute("category")
        self.icon = self._get_attribute("icon")
        self.description = self._get_attribute("description")
        self._initialize_stats()
        self.max_health_points = self.health_points
        self.level = int(self._get_attribute("level") or 0)
        self.physical_attack_power = int(self._get_attribute("physical_attack_power") or 0)
        self.spiritual_power = int(self._get_attribute("spiritual_power") or 0)
        self.attack_range = int(self._get_attribute("attack_range"))
        self.skills = self._get_attribute("skills")
        # Weapon initialization
        weapon = _parse_attribute(self.data_creatures, "weapon")
        if weapon is not None:
            self.weapon = Weapon(weapon)
        else:
            self.weapon = None

    """Retrieves an attribute value from the loaded data."""
    def _get_attribute(self, attribute_name):
        return _parse_attribute(self.data_creatures, attribute_name)

    """Initializes health, defense, and agility stats from limits or reserved values."""
    def _initialize_stats(self):
        stats = LimitsStats.get_stats(self.category)
        if stats:
            self.health_points = _generate_random_value(*stats["health_points"])
            self.defense = _generate_random_value(*stats["defense"])
            self.agility = _generate_random_value(*stats["agility"])
        else:
            self.health_points = int(self._get_attribute("health_points") or 0)
            self.defense = int(self._get_attribute("defense") or 0)
            self.agility = int(self._get_attribute("agility") or 0)

    """Heals the creature by the given number of points."""
    def healing(self, points):
        if self.health_points + points >= self.max_health_points:
            self.health_points = self.max_health_points
        else:
            self.health_points += points

    """Performs a physical attack on the target."""
    def attack_with_strength(self, enemy: "Creature"):
        self._attack(enemy, self.physical_attack_power)

    """Performs a spiritual attack on the target."""
    def attack_with_spirit(self, enemy: "Creature"):
        self._attack(enemy, self.spiritual_power)

    """Calculates and applies the result of an attack."""
    def _attack(self, enemy, attack):
        result_dice = random.randint(1, 20)

        attack += self._apply_weapon_damage(attack)
        efficiency_chance = self.calculate_hit_chance(enemy, attack, result_dice)
        random_factor = random.random()

        if result_dice == 20 or (result_dice != 1 and random_factor <= efficiency_chance):
            _apply_damage_to_enemy(enemy, attack)
            self._check_weapon_durability()

    """Calculates the chance to successfully hit the target."""
    def calculate_hit_chance(self, enemy, attack, result_dice):
        attack_points = result_dice + self.level + attack
        defense_points = enemy.level + enemy.agility

        efficiency_chance = (attack_points - defense_points + MAX_ATTACK_POINTS) / (2 * MAX_ATTACK_POINTS)
        self.HIT_CHANCE = efficiency_chance
        return self._clamp_chance(efficiency_chance)

    """Clamps the hit chance to a minimum of 10% and a maximum of 90%."""
    def _clamp_chance(self, efficiency_chance):
        if efficiency_chance > 0.9:
            return 0.9
        elif efficiency_chance < 0.1:
            return 0.1
        else:
            return efficiency_chance

    """Applies the weapon's bonus to the attack if it is not broken and used."""
    def _apply_weapon_damage(self, attack):
        if self.weapon and not self.weapon.is_break and attack != self.spiritual_power:
            return self.weapon.strike_power
        return 0

    """Reduces weapon durability and marks it as broken if durability reaches zero."""
    def _check_weapon_durability(self):
        if self.weapon:
            self.weapon.durability -= 1
            if self.weapon.durability == 0:
                self.weapon.is_break = True
