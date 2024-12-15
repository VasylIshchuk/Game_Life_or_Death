from creature import *


class Rat(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy):
        is_hit = super().attack(enemy)
        if is_hit is True: enemy.add_poison_effect(3)
