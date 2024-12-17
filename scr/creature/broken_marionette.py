from .creature import Creature


class BrokenMarionette(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy):
        """Perform attack on the target and apply healing if attack hits."""
        is_hit = super().attack(enemy)
        if is_hit is True: self.healing(2)
