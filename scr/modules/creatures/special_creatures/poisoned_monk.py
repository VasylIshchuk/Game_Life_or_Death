from ..creature import Creature
from ..hero import Hero

EXPLODE_RANGE_RADIUS = 3


class PoisonedMonk(Creature):
    def __init__(self, title):
        super().__init__(title)

    def apply_abilities(self, enemy: Hero):
        """TODO: Apply abilities when the monk is dead and within explosion range."""
        if not self.is_alive and self.is_within_range(enemy, EXPLODE_RANGE_RADIUS):
            self._apply_damage_to_enemy(enemy, self.attack_power * 2)
