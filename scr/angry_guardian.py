from creature import *


class AngryGuardian(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.bonus_attack = 0

    def attack(self, enemy):
        result_dice = random.randint(1, 20)

        attack = self.attack_power + self.bonus_attack
        efficiency_chance = self.calculate_hit_chance(enemy, attack, result_dice)
        random_factor = random.random()

        if result_dice == 20 or (result_dice != 1 and random_factor <= efficiency_chance):
            self._apply_damage_to_enemy(enemy, attack)
