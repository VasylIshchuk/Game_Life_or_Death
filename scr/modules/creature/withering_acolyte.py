from .creature import Creature
import random

ROUND_FOR_DOUBLE_HIT = 3


class WitheringAcolyte(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_hits = 1

    def attack(self, enemy):
        result_dice = self._roll_dice()
        attack_power = self._get_hit()

        hit_probability = self._calculate_hit_probability(enemy, attack_power, result_dice)
        random_factor = random.random()

        if self._perform_attack_check(enemy, result_dice, random_factor, hit_probability):
            self._apply_damage_to_enemy(enemy, self.attack_power)

        self.count_hits += 1

    def _get_hit(self):
        attack_power = self.attack_power
        if not self.count_hits % ROUND_FOR_DOUBLE_HIT:
            attack_power *= 2
            self.count_hit = 0
        return attack_power
