from .creature import Creature
from .hero import Hero

MAX_ATTACK_POWER_INCREASE = 5


class AngryGuardian(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_bonus_attack = 0

    def attack(self, enemy: Hero):
        super().attack(enemy)

    def apply_abilities(self):
        if self.count_bonus_attack != MAX_ATTACK_POWER_INCREASE:
            self._increase_attack_power()
            self.count_bonus_attack += 1

    def _increase_attack_power(self):
        self.attack_power += 1
