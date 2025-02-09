from ..creature import Creature
from ..hero import Hero

POISON_ROUNDS = 3


class Rat(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy: Hero, game_map=None):
        is_hit = super().attack(enemy)
        self._apply_abilities(enemy, is_hit)

    def _apply_abilities(self, enemy: Hero, is_hit):
        if is_hit is True: enemy.apply_poison_effect(POISON_ROUNDS)
