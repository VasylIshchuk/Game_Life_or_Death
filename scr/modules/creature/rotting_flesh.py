from .creature import Creature

ROUND_FOR_SUMMON = 3
CREATURE_SUMMON = 2


class RottingFlesh(Creature):
    def __init__(self, title):
        super().__init__(title)
        self.count_hit = 1

    def attack(self, enemy):
        """Attack enemy, decrease mental state and summon creatures."""
        is_hit = super().attack(enemy)
        self._apply_abilities(enemy, is_hit)
        self._summon_creatures()

    def _apply_abilities(self, enemy, is_hit):
        """Decrease mental state"""
        if is_hit is True:
            enemy.mental_state -= self.level
            enemy.check_mental_state()
        self.count_hit += 1

    def _summon_creatures(self):
        """Summon creatures after certain number of hits."""
        if not self.count_hit % ROUND_FOR_SUMMON:
            for x in range(CREATURE_SUMMON):
                creature = Creature("The Rotting of Life")
                # add to map
                # creature.set_position()
