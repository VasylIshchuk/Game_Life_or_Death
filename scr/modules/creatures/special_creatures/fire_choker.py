from ..creature import Creature
from ..hero import Hero

FIRE_RANGE_RADIUS = 2
FIRE_DAMAGE = 3


class FireChoker(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy: Hero):
        super().attack(enemy)
        self.apply_abilities(enemy)

    def apply_abilities(self, enemy: Hero):
        """TODO: Apply fire damage if target is within range."""
        # if self.is_within_range(enemy, FIRE_RANGE_RADIUS):
        #     enemy.health_points -= FIRE_DAMAGE
        #     enemy.check_is_alive()
