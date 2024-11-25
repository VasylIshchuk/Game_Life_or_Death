from game_entity import GameEntity
from inventory import Inventory
from weapon import Weapon
from itemFactory import ItemFactory

import random


class Creature(GameEntity):
    def __init__(self, title):
        super().__init__(title)

        data_creature = GameEntity.load_data_from_file("../creatures.json", title)

        self.is_live = True
        self.attack_range_spirit_power = 2
        if title == 'Mark':
            self.mental_state = self.parse_attribute(data_creature, "mental_state")
            self.inventory = Inventory()

        self.category = self.parse_attribute(data_creature, "category")
        self.icon = self.parse_attribute(data_creature, "icon")
        self.description = self.parse_attribute(data_creature, "description")
        self.health_points = int(self.parse_attribute(data_creature, "health_points") or 0)
        self.level = int(self.parse_attribute(data_creature, "level") or 0)
        self.defense = int(self.parse_attribute(data_creature, "defense") or 0)
        self.strike_power = int(self.parse_attribute(data_creature, "strike_power") or 0)
        self.spiritual_power = int(self.parse_attribute(data_creature, "spiritual_power") or 0)
        self.attack_range = int(self.parse_attribute(data_creature, "attack_range") or 0)
        self.agility = int(self.parse_attribute(data_creature, "agility") or 0)
        self.skills = self.parse_attribute(data_creature, "skills")

        weapon = self.parse_attribute(data_creature, "weapon")
        if weapon is not None:
            self.weapon = Weapon(weapon)
        else:
            self.weapon = None

    def heal(self, points):
        if self.health_points + points >= 100:
            self.health_points = 100
        else:
            self.health_points += points

    def attack_strength(self, enemies: "Creature"):
        self._attack(enemies, self.strike_power)

    def attack_spirit_power(self, enemies: "Creature"):
        self._attack(enemies, self.spiritual_power)

    def _attack(self, enemy, attack):
        result_dice = random.randint(1, 20)
        attack_points = result_dice + self.level + attack
        defense_points = enemy.level + enemy.agility
        if result_dice == 20 or (result_dice != 1 and attack_points >= defense_points):
            self._apply_weapon_damage(attack)
            self._apply_damage_to_enemy(enemy, attack)

    def _apply_weapon_damage(self, attack):
        if self.weapon and not self.weapon.is_break and attack != self.spiritual_power:
            attack += self.weapon.strike_power
            self._check_weapon_durability()

    def _check_weapon_durability(self):
        if --self.weapon.durability == 0:
            self.weapon.is_break = True

    def _apply_damage_to_enemy(self, enemy, attack):
        if enemy.defense > 0:
            if enemy.defense >= attack:
                enemy.health_points -= attack
            else:
                enemy.health_points -= attack - enemy.defense
                enemy.defense = 0
        elif enemy.health_points > attack:
            enemy.health_points -= attack
        else:
            enemy.health_points = 0
            enemy.is_live = False


cre1 = Creature("Mark")
weap = ItemFactory.create_item("Axe")
cre1.weapon = weap
cre2 = Creature("Rat")
print(f"szczur: {cre2.health_points}; hero: {cre1.health_points} ")
cre1.attack_spirit_power(cre2)
print(f"szczur: {cre2.health_points}; hero: {cre1.health_points}")
cre1.attack_strength(cre2)
print(f"szczur: {cre2.health_points}; hero: {cre1.health_points}")
