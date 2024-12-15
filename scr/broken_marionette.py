from creature import *


class Rat(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy):
        is_hit = super().attack(enemy)
        if is_hit is True:
            enemy.health_points -= 2
            enemy.check_is_alive()
            self.healing(2)