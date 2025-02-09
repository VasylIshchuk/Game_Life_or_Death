import random

from ..creature import Creature
from ..hero import Hero
from ...core.data_loader import load_data_from_file

ROUND_FOR_SUMMON = 5


class TempleGuardian(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_rounds = 0

    def attack(self, enemy: Hero, game_map=None):
        super().attack(enemy)
        self._summon_creatures(game_map)
        self.count_rounds += 1

    def _summon_creatures(self, game_map):
        if not self.count_rounds % ROUND_FOR_SUMMON:
            self.count_rounds = 0
            creatures = load_data_from_file("./creatures.json")
            creature_title = random.choice(creatures)
            creature = Creature(creature_title)
            position = game_map.get_random_valid_position(self)
            if position:
                game_map.place_creature(creature, position)
