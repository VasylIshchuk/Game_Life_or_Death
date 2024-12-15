from creature import *


class PsychologicalEnemy(Creature):
    def __init__(self, title):
        super().__init__(title)

    def attack(self, enemy):
        is_hit = super().attack(enemy)
        if is_hit is True:
            enemy.mental_state  -= self.level
