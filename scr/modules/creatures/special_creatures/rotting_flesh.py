from ..creature import Creature
from ..hero import Hero
from ...maps.position import Position

ROUND_FOR_SUMMON = 3
CREATURE_SUMMON = 2


class RottingFlesh(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_rounds = 0

    def attack(self, enemy: Hero, game_map=None):
        is_hit = super().attack(enemy)
        self._apply_abilities(enemy, is_hit, game_map)
        self.count_rounds += 1

    def _apply_abilities(self, enemy: Hero, is_hit, game_map):
        if is_hit is True:
            enemy.decrease_mental_state(self.level)
        self._summon_creatures(game_map)

    def _summon_creatures(self, game_map):
        if not self.count_rounds % ROUND_FOR_SUMMON:
            self.count_rounds = 0
            for x in range(CREATURE_SUMMON):
                creature = Creature("The Rotting of Life")
                position =  game_map.get_random_valid_position(self)
                if position:
                    game_map.place_creature(creature,position)
