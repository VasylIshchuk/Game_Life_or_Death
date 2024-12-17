from .creature import Creature

POISON_ROUNDS = 3


class Rat(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy):
        """Method for the rat to attack an enemy. If the attack hits, the enemy is poisoned."""
        is_hit = super().attack(enemy)
        if is_hit is True: enemy.apply_poison(POISON_ROUNDS)
