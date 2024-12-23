from .creature import Creature


class Psychological(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy):
        is_hit = super().attack(enemy)
        self._apply_abilities(enemy,is_hit)

    def _apply_abilities(self, enemy, is_hit):
        """Decrease mental state"""
        if is_hit is True:
            enemy.mental_state -= self.level
            enemy.check_mental_state()