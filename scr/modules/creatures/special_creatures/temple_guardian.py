import random

from ..creature import Creature
from ..hero import Hero
from ...core.data_loader import load_data_from_file
from ...maps.position import Position

ROUND_FOR_SUMMON = 5


class TempleGuardian(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_rounds = 0

    def attack(self, enemy: Hero):
        is_hit = super().attack(enemy)
        self._apply_abilities(enemy, is_hit)
        self.count_rounds += 1

    def _apply_abilities(self, enemy: Hero, is_hit):
        self._summon_creatures()

    def _summon_creatures(self):
        """TODO: add to map and creature.set_position()"""
        if not self.count_rounds % ROUND_FOR_SUMMON:
            self.count_rounds = 0
            creatures = load_data_from_file("./creatures.json")
            creature_title = random.choice(creatures)
            creature = Creature(creature_title)
            position = Position(self.get_x_position(), self.get_y_position())
