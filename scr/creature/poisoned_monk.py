from .creature import Creature

EXPLODE_RANGE_RADIUS = 3


class PoisonedMonk(Creature):
    def __init__(self, title):
        super().__init__(title)

    def apply_skills(self, enemy):
        """Apply skills when the monk is dead and within explosion range."""
        if not self.is_alive and self.is_within_range(enemy, EXPLODE_RANGE_RADIUS):
            enemy.health_points -= enemy.attack_power * 2
            enemy.check_is_alive()
