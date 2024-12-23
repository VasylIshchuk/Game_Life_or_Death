from .creature import Creature


class BrokenMarionette(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy):
        """Perform attack on the target"""
        is_hit = super().attack(enemy)
        self._apply_abilities(is_hit)

    def _apply_abilities(self, is_hit):
        """Apply healing if attack hits"""
        if is_hit is True: self.healing(2)
