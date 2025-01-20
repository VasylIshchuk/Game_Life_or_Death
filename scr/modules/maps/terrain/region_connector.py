from .drunkard_walk import DrunkardWalker
from ..direction import Direction
from ...core.icons import Icon

PROBABILITY_TOWARD_GOAL = 1


class RegionConnector(DrunkardWalker):
    def __init__(self, game_map, start_position_regions):
        super().__init__(game_map)
        self._start_position_regions = start_position_regions
        self.goal_position = None

    def connect_regions(self, regions_quantity):
        for region_index in range(regions_quantity - 1):
            self._set_drunkard_position(region_index)
            self.goal_position = self._start_position_regions[region_index + 1]

            while not self._has_reached_goal():
                self._navigate_toward_goal()

    def _set_drunkard_position(self, region_index):
        self._drunkard_position = self._start_position_regions[region_index]

    def _has_reached_goal(self):
        return (self._drunkard_position.get_x() == self.goal_position.get_x() and
                self._drunkard_position.get_y() == self.goal_position.get_y())

    def _navigate_toward_goal(self):
        self._reset_direction_probabilities()
        self._adjust_probabilities_toward_goal()
        self._normalize_direction_probabilities()
        self._choose_direction()
        self._make_hall()

    def _adjust_probabilities_toward_goal(self):
        self._bias_probability(Direction.EAST, Direction.WEST, self._drunkard_position.get_x(),
                               self.goal_position.get_x(), PROBABILITY_TOWARD_GOAL)
        self._bias_probability(Direction.SOUTH, Direction.NORTH, self._drunkard_position.get_y(),
                               self.goal_position.get_y(), PROBABILITY_TOWARD_GOAL)

    def _make_hall(self):
        new_position = self._get_tile_in_direction(self._drunkard_position, self._current_direction)
        if self._is_within_bounds(new_position):
            self._drunkard_position = new_position
            self._map.set_cell_icon(self._drunkard_position, Icon.GROUND)
