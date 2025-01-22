from .drunkard_walk import DrunkardWalker
from ..direction import Direction
from ..position import Position
from ...core.icons import Icon

IMPASSABLE_ICONS = {Icon.TREE, Icon.STONE}

PERCENT_GOAL = 0.12
MAX_WALK_ITERATIONS = 25000

PROBABILITY_TOWARD_PREVIOUS_DIRECTION = 0.3
PROBABILITY_TOWARD_NEW_TERRITORY = 0.5


class RegionGenerator(DrunkardWalker):
    def __init__(self, game_map):
        super().__init__(game_map)

        self._max_walk_iterations = max(MAX_WALK_ITERATIONS, self._width * self._height * 10)
        self._filled_goal = self._width * self._height * PERCENT_GOAL
        self._count_filled_cells = 0

        self._previous_direction = None

    def generate_region(self, start_position):
        self._drunkard_position = start_position
        self._generate_drunkards_walk()

    def _generate_drunkards_walk(self):
        for _ in range(self._max_walk_iterations):
            self._take_step()
            if self._count_filled_cells >= self._filled_goal:
                break

    def _take_step(self):
        self._update_direction_probabilities()
        self._choose_direction()
        self._move_drunkard()

    def _update_direction_probabilities(self):
        self._reset_direction_probabilities()
        self._apply_previous_direction_bias()
        self._apply_new_territory_probability()
        self._normalize_direction_probabilities()

    def _apply_previous_direction_bias(self):
        if self._previous_direction:
            self._direction_probabilities[self._previous_direction] += PROBABILITY_TOWARD_PREVIOUS_DIRECTION

    def _apply_new_territory_probability(self):
        for direction in self._direction_probabilities:
            next_position = self._get_tile_in_direction(self._drunkard_position, direction)
            if self._has_sufficient_unexplored_neighbors(next_position):
                self._direction_probabilities[direction] += PROBABILITY_TOWARD_NEW_TERRITORY

    def _has_sufficient_unexplored_neighbors(self, position):
        adjacent_tiles = self._get_adjacent_tiles(position)
        count_unexplored_neighbors = 0
        for tile in adjacent_tiles:
            if not tile == position and self._can_carve(tile):
                count_unexplored_neighbors += 1
        return count_unexplored_neighbors >= 2

    def _get_adjacent_tiles(self, position):
        return [
            self._get_tile_in_direction(position, Direction.NORTH),
            self._get_tile_in_direction(position, Direction.SOUTH),
            self._get_tile_in_direction(position, Direction.EAST),
            self._get_tile_in_direction(position, Direction.WEST),
        ]

    def _can_carve(self, position: Position):
        icon = self._map.get_cell_icon(position)
        return icon in IMPASSABLE_ICONS

    def _move_drunkard(self):
        new_position = self._get_tile_in_direction(self._drunkard_position, self._current_direction)
        if self._is_within_bounds(new_position):
            self._drunkard_position = new_position
            if self._can_carve(new_position):
                self._map.set_cell_icon(self._drunkard_position, Icon.GROUND)
                self._count_filled_cells += 1
            self._previous_direction = self._current_direction
