import json

from game_entity import GameEntity
from inventory import Inventory
from weapon import Weapon

import random


class Creature(GameEntity):

    def __init__(self, title):
        super().__init__(title)

        self.data_creature = GameEntity.load_data_from_file("../creatures.json", title)

        self.is_live = True
        self.attack_range_spirit_power = 2
        if title == 'Mark':
            self.mental_state = self.parse_attribute(self.data_creature, "mental_state")
            self.inventory = Inventory()

        self.category = self.parse_attribute(self.data_creature, "category")
        self.icon = self.parse_attribute(self.data_creature, "icon")
        self.description = self.parse_attribute(self.data_creature, "description")
        self.health_points = int(self.parse_attribute(self.data_creature, "health_points"))
        self.level = int(self.parse_attribute(self.data_creature, "level") or 0)
        self.defense = int(self.parse_attribute(self.data_creature, "defense") or 0)
        self.strike_power = int(self.parse_attribute(self.data_creature, "strike_power") or 0)
        self.spiritual_power = int(self.parse_attribute(self.data_creature, "spiritual_power") or 0)
        self.attack_range = int(self.parse_attribute(self.data_creature, "attack_range"))
        self.agility = int(self.parse_attribute(self.data_creature, "agility") or 0)
        self.skills = self.parse_attribute(self.data_creature, "skills")

        weapon = self.parse_attribute(self.data_creature, "weapon")
        if weapon is not None:
            self.weapon = Weapon(weapon)
        else:
            self.weapon = None

    def heal(self, points):
        max_health_points = int(self.parse_attribute(self.data_creature, "health_points") or 0)
        if self.health_points + points >= max_health_points:
            self.health_points = max_health_points
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

    @staticmethod
    def test_heal():
        mark = Creature("Mark")
        mark.health_points = 90
        print(f"Health points of {mark.title} = {mark.health_points}")

        heal_points = 2
        mark.heal(heal_points)
        print(f"After healing by {heal_points} points: health points of {mark.title} = {mark.health_points}")

        heal_points = 10
        mark.heal(heal_points)
        print(f"After healing by {heal_points} points: health points of {mark.title} = {mark.health_points}")

    @staticmethod
    def test_attack_strength():
        creatures = Creature._load_all_creatures()
        Creature._print_new_line()
        creature_1 = Creature(creatures[Creature._select_creature_for_fight(creatures)])
        Creature._print_new_line()
        creature_2 = Creature(creatures[Creature._select_creature_for_fight(creatures)])
        Creature._print_new_line()
        Creature._print_new_line()
        attack_count = Creature._quantity_attacks()
    ######################## attack

    @staticmethod
    def _load_all_creatures():
        try:
            with open("../creatures.json", "r") as file:
                data = json.load(file)
                return Creature._show_all_creatures(data)
        except FileNotFoundError:
            print("File not found")
            raise
        except json.JSONDecodeError:
            print("Invalid JSON format")
            raise

    @staticmethod
    def _show_all_creatures(data):
        creatures =[]
        for idx, creature in enumerate(data, start=1):
            print(f"{idx}) {creature}")
            creatures.append(creature)
        return creatures

    @staticmethod
    def _select_creature_for_fight(creatures) -> int:
        while True:
            try:
                print("Select a creature by its number: ", end="")
                index = int(input()) - 1
                if 0 <= index < len(creatures):
                    return index
                print("Invalid number. Please select a valid creature number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def _quantity_attacks():
        while True:
            try:
                attack_count = int(input("Enter the number of attacks: "))
                if attack_count > 0:
                    return attack_count
                print("The number of attacks must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def _print_new_line():
        print()
