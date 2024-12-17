from .creature import Creature
import random

class AngryGuardian(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.bonus_attack = 0

    def attack(self, enemy):
        result_dice = random.randint(1, 20)

        attack_power = self.attack_power + self.bonus_attack
        hit_chance = self.calculate_hit_chance(enemy, attack_power, result_dice)
        random_factor = random.random()

        if result_dice == 20 or (result_dice != 1 and random_factor <= hit_chance):
            self._apply_damage_to_enemy(enemy, attack_power)

    def apply_skills(self):
        if self.bonus_attack != 5: self.bonus_attack += 1
