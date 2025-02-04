from ..creature import Creature
from ..hero import Hero
from ...maps.position import Position

ROUND_FOR_SUMMON = 3
CREATURE_SUMMON = 2


class RottingFlesh(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_rounds = 0

    def attack(self, enemy: Hero):
        is_hit = super().attack(enemy)
        self._apply_abilities(enemy, is_hit)
        self.count_rounds += 1

    def _apply_abilities(self, enemy: Hero, is_hit):
        if is_hit is True:
            enemy.decrease_mental_state(self.level)
        self._summon_creatures()

    def _summon_creatures(self):
        """TODO: add to map and creature.set_position()"""
        if not self.count_rounds % ROUND_FOR_SUMMON:
            self.count_rounds = 0
            for x in range(CREATURE_SUMMON):
                creature = Creature("The Rotting of Life")
                position = Position(self.get_x_position(), self.get_y_position())
