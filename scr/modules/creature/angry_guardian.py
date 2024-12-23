from .creature import Creature
import random

class AngryGuardian(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.bonus_attack = 0

    def attack(self, enemy):
        result_dice = self._roll_dice()

        attack_power = self.attack_power + self.bonus_attack
        hit_probability = self._calculate_hit_probability(enemy, attack_power, result_dice)
        random_factor = random.random()

        if self._perform_attack_check(enemy, result_dice, random_factor, hit_probability):
            self._apply_damage_to_enemy(enemy, self.attack_power)

    def apply_abilities(self):
        if self.bonus_attack != 5: self.bonus_attack += 1
