from ..maps.position import Position
from .special_creatures.rotting_flesh import RottingFlesh
from .special_creatures.temple_guardian import TempleGuardian

VISIBLE_RANGE = 4
SPECIAL_CREATURES = (
    RottingFlesh,
    TempleGuardian
)


class AIController:
    def __init__(self, creature):
        self.creature = creature

    def make_decision(self, enemy, game_map):
        if self.creature.is_within_range(enemy, self.creature.attack_range):
            self._creature_attack(enemy, game_map)
        if self.creature.is_within_range(enemy, VISIBLE_RANGE):
            new_position = self._get_next_position_towards_enemy(enemy)
            if self._try_move(game_map, new_position): return

        new_position = game_map.get_random_valid_position(self.creature)
        if new_position:
            game_map.move_creature(self.creature, new_position)

    def _creature_attack(self, enemy, game_map):
        if isinstance(self.creature, SPECIAL_CREATURES):
            self.creature.attack(enemy, game_map)
        else:
            self.creature.attack(enemy)
        self._validate_is_alive(enemy, game_map)

    def _validate_is_alive(self, creature, game_map):
        if not creature.is_alive: game_map.remove_creature(creature)

    def _get_next_position_towards_enemy(self, enemy):
        dx = (enemy.get_x_position() > self.creature.get_x_position()) - (
                enemy.get_x_position() < self.creature.get_x_position())
        dy = (enemy.get_y_position() > self.creature.get_y_position()) - (
                enemy.get_y_position() < self.creature.get_y_position())
        return Position(self.creature.get_x_position() + dx, self.creature.get_y_position() + dy)

    def _try_move(self, game_map, new_position):
        if game_map.is_placement_valid(new_position):
            game_map.move_creature(self.creature, new_position)
            return True
        return False
