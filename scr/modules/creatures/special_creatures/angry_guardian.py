from ..creature import Creature
from ..hero import Hero

MAX_ATTACK_POWER_INCREASE = 5


class AngryGuardian(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_bonus_attack = 0

    def attack(self, enemy: Hero, game_map=None):
        super().attack(enemy)

    def apply_abilities(self):
        if self.count_bonus_attack != MAX_ATTACK_POWER_INCREASE:
            self.increase_attack_power(1)
            self.count_bonus_attack += 1

