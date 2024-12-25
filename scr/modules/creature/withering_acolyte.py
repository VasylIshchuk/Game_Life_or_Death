from .creature import Creature

ROUND_FOR_DOUBLE_HIT = 3


class WitheringAcolyte(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_hits = 1

    def attack(self, enemy):
        is_hit = super().attack(enemy)
        if self._check_ability_usage() and is_hit:
            self._apply_abilities(enemy)
        self.count_hits += 1

    def _check_ability_usage(self):
        if not self.count_hits % ROUND_FOR_DOUBLE_HIT:
            self.count_hits = 1
            return True
        return False

    def _apply_abilities(self, enemy):
        self._double_attack_power(enemy)

    def _double_attack_power(self, enemy):
        self._apply_damage_to_enemy(enemy, self.attack_power)
