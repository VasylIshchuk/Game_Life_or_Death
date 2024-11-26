from game_entity import GameEntity
from inventory import Inventory
from weapon import Weapon

import random


class Creature(GameEntity):
    """Initializes a creature with attributes loaded from a data file."""

    def __init__(self, title):
        super().__init__(title)

        self.data_creatures = GameEntity.load_data_from_file("../creatures.json", title)

        self.is_alive = True
        self.attack_range_spirit_power = 2
        # Special handling for "Mark"
        if title == 'Mark':
            self.mental_state = self.parse_attribute(self.data_creatures, "mental_state")
            self.inventory = Inventory()
        # General attributes
        self.category = self.get_attribute("category")
        self.icon = self.get_attribute("icon")
        self.description = self.get_attribute("description")
        self.health_points = int(self.get_attribute("health_points"))
        self.max_health_points = self.health_points
        self.level = int(self.get_attribute("level") or 0)
        self.defense = int(self.get_attribute("defense") or 0)
        self.physical_attack_power = int(self.get_attribute("physical_attack_power") or 0)
        self.spiritual_power = int(self.get_attribute("spiritual_power") or 0)
        self.attack_range = int(self.get_attribute("attack_range"))
        self.agility = int(self.get_attribute("agility") or 0)
        self.skills = self.get_attribute("skills")
        # Weapon initialization
        weapon = self.parse_attribute(self.data_creatures, "weapon")
        if weapon is not None:
            self.weapon = Weapon(weapon)
        else:
            self.weapon = None

    def get_attribute(self, attribute_name):
        return self.parse_attribute(self.data_creatures, attribute_name)

    """Heals the creature by the given number of points."""
    def healing(self, points):
        if self.health_points + points >= self.max_health_points:
            self.health_points = self.max_health_points
        else:
            self.health_points += points

    """Performs a physical attack on the target."""
    def attack_with_strength(self, enemies: "Creature"):
        self._attack(enemies, self.physical_attack_power)

    """Performs a spiritual attack on the target."""
    def attack_with_spirit(self, enemies: "Creature"):
        self._attack(enemies, self.spiritual_power)

    """Calculates and applies the result of an attack."""
    def _attack(self, enemy, attack):
        result_dice = random.randint(1, 20)
        attack_points = result_dice + self.level + attack
        defense_points = enemy.level + enemy.agility
        if result_dice == 20 or (result_dice != 1 and attack_points >= defense_points):
            self._apply_weapon_damage(attack)
            self._apply_damage_to_enemy(enemy, attack)

    """Applies the weapon's bonus to the attack if it is not broken and used."""
    def _apply_weapon_damage(self, attack):
        if self.weapon and not self.weapon.is_break and attack != self.spiritual_power:
            attack += self.weapon.physical_attack_power
            self._check_weapon_durability()

    """Reduces weapon durability and marks it as broken if it reaches zero."""
    def _check_weapon_durability(self):
        if --self.weapon.durability == 0:
            self.weapon.is_break = True

    """Applies damage to the target considering its defense."""
    def _apply_damage_to_enemy(self, enemy, attack):
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
