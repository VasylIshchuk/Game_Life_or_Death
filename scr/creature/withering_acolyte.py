from .creature import Creature
import random

ROUND_FOR_DOUBLE_HIT = 3


class WitheringAcolyte(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_hit = 1

    def attack(self, enemy):
        result_dice = random.randint(1, 20)
        attack_power = self._get_hit()

        efficiency_chance = self.calculate_hit_chance(enemy, attack_power, result_dice)
        random_factor = random.random()

        if result_dice == 20 or (result_dice != 1 and random_factor <= efficiency_chance):
            self._apply_damage_to_enemy(enemy, attack_power)
            self.count_hit += 1

    def _get_hit(self):
        attack_power = self.attack_power
        if not self.count_hit % ROUND_FOR_DOUBLE_HIT:
            attack_power *= 2
            self.count_hit = 0
        return attack_power
