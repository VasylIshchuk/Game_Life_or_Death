from collections import deque

from ..grid import Grid
from ..position import Position
from ..direction import Direction
from ...core.icons import Icon


class BFS:
    def __init__(self, game_map):
        self._map = game_map
        self._width = self._map.get_map_width()
        self._height = self._map.get_map_height()
        self._visited = Grid(False, self._width, self._height)

    def find_nearest_point(self, start_position):
        queue = deque([start_position])

        self._visited.set_value(start_position, True)

        while queue:
            position = queue.popleft()

            for direction in Direction.DIRECTIONS:
                neighbor_position = self._get_neighbor_position(position, direction)

                if self._can_visit(neighbor_position):
                    if self._is_ground(neighbor_position):
                        return neighbor_position

                    queue.append(neighbor_position)
                    self._visited.set_value(neighbor_position, True)

    def _get_neighbor_position(self, position, direction):
        neighbor_x = position.get_x() + direction.get_x()
        neighbor_y = position.get_y() + direction.get_y()
        return Position(neighbor_x, neighbor_y)

    def _can_visit(self, position):
        return self._is_within_bounds(position) and not self._is_visited(position)

    def _is_within_bounds(self, position):
        return 0 <= position.get_x() < self._width and 0 <= position.get_y() < self._height

    def _is_visited(self, position):
        return self._visited.get_value(position)

    def _is_ground(self, position):
        return self._map.get_cell_icon(position) == Icon.GROUND
