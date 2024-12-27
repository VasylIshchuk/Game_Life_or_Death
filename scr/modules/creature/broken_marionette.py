from .creature import Creature
from .hero import Hero


class BrokenMarionette(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy: Hero):
        is_hit = super().attack(enemy)
        self._apply_abilities(is_hit)

    def _apply_abilities(self, is_hit):
        if is_hit is True: self.healing(2)
