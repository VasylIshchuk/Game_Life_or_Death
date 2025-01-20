import random

from ..position import Position
from ..direction import Direction

INITIAL_DIRECTION_WEIGHT = 1.0


class DrunkardWalker:

    def __init__(self, game_map):
        self._map = game_map
        self._width = self._map.get_map_width()
        self._height = self._map.get_map_height()

        self._drunkard_position = None
        self._current_direction = None

        self._direction_probabilities = {
            Direction.NORTH: INITIAL_DIRECTION_WEIGHT,
            Direction.SOUTH: INITIAL_DIRECTION_WEIGHT,
            Direction.EAST: INITIAL_DIRECTION_WEIGHT,
            Direction.WEST: INITIAL_DIRECTION_WEIGHT,
        }

    def _reset_direction_probabilities(self):
        for direction in self._direction_probabilities:
            self._direction_probabilities[direction] = INITIAL_DIRECTION_WEIGHT

    def _get_tile_in_direction(self, position, direction):
        x = position.get_x() + direction.get_x()
        y = position.get_y() + direction.get_y()
        new_position = Position(x, y)
        if not self._is_within_bounds(new_position): return position
        return new_position

    def _normalize_direction_probabilities(self):
        total_probability = sum(self._direction_probabilities.values())
        for direction in self._direction_probabilities:
            self._direction_probabilities[direction] /= total_probability

    def _choose_direction(self):
        random_value = random.random()
        cumulative_probability = 0
        for direction, probability in self._direction_probabilities.items():
            cumulative_probability += probability
            if random_value < cumulative_probability:
                self._current_direction = direction
                break

    def _bias_probability(self, forward_direction, backward_direction, current_position, target_position, bias_value):
        if current_position < target_position:
            self._direction_probabilities[forward_direction] += bias_value
        elif current_position > target_position:
            self._direction_probabilities[backward_direction] += bias_value

    def _is_within_bounds(self, position):
        return 0 < position.get_x() < self._width - 1 and 0 < position.get_y() < self._height - 1
