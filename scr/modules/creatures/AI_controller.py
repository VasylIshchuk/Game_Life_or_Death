import random

from ..maps.position import Position
from .special_creatures.rotting_flesh import RottingFlesh
from .special_creatures.temple_guardian import TempleGuardian

VISIBLE_RANGE = 4

SPECIAL_CREATURES = (
    RottingFlesh,
    TempleGuardian
)

UNMOVED_CREATURES = {
    "Statue"
}


class AIController:
    def __init__(self, creature):
        self.creature = creature

    def make_decision(self, enemy, game_map):
        if (self.creature.is_within_range(enemy, self.creature.attack_range, game_map) and
                (self._is_above_critical_health() or self._fifty_fifty())):
                self._creature_attack(enemy, game_map)
                return

        if self.creature.title in UNMOVED_CREATURES: return

        if self.creature.is_within_range(enemy, VISIBLE_RANGE, game_map) and self._is_above_critical_health():
            new_position = self._get_next_position_towards_enemy(enemy)
            if game_map.place_creature(self.creature, new_position): return

        new_position = game_map.get_random_valid_position(self.creature)
        if new_position:
            game_map.place_creature(self.creature, new_position)

    def _creature_attack(self, enemy, game_map):
        if isinstance(self.creature, SPECIAL_CREATURES):
            self.creature.attack(enemy, game_map)
        else:
            self.creature.attack(enemy)

    def _is_above_critical_health(self):
        return self.creature.health_points > self.creature.max_health_points * 0.25

    def _fifty_fifty(self):
        return random.random() > 0.5

    def _get_next_position_towards_enemy(self, enemy):
        dx = (enemy.get_x_position() > self.creature.get_x_position()) - (
                enemy.get_x_position() < self.creature.get_x_position())
        dy = (enemy.get_y_position() > self.creature.get_y_position()) - (
                enemy.get_y_position() < self.creature.get_y_position())
        return Position(self.creature.get_x_position() + dx, self.creature.get_y_position() + dy)
