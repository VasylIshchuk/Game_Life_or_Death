import random

from ..position import Position
from ...core.icons import Icon
from ..direction import Direction
from .constants import WINDING_PROBABILITY

LAST_ELEMENT = -1


def _get_cell(position: Position, direction, step):
    x = _calculate_new_coordinate(position.get_x(), direction.get_x(), step)
    y = _calculate_new_coordinate(position.get_y(), direction.get_y(), step)
    return Position(x, y)


def _calculate_new_coordinate(base, offset, step):
    return base + offset * step


class Corridor:
    def __init__(self, temple):
        self.temple = temple
        self._pending_cells = []
        self._last_direction = None

    def generate_corridor(self, start_position: Position):
        self._initialize_starting_position(start_position)
        self._pending_cells.append(start_position)

        while self._pending_cells:
            self._handle_cell()

    def _initialize_starting_position(self, start_position):
        self.temple.increase_region_index()
        self.temple.carve(start_position, Icon.CORRIDOR_FLOOR)

    def _handle_cell(self):
        current_cell = self._pending_cells[LAST_ELEMENT]
        available_directions = self._get_available_directions(current_cell)

        if available_directions:
            self._navigate_to_new_cell(current_cell, available_directions)
        else:
            self._backtrack()

    def _get_available_directions(self, cell):
        available_directions = set()
        for direction in Direction.DIRECTIONS:
            if self._can_carve(cell, direction):
                available_directions.add(direction)
        return available_directions

    def _can_carve(self, position: Position, direction):
        if self._is_within_bounds(position, direction):
            return self._leads_to_wall(position, direction)
        return False

    def _is_within_bounds(self, position: Position, direction):
        cell = _get_cell(position, direction, 3)
        if (0 <= cell.get_x() < self.temple.get_map_width()) and (0 <= cell.get_y() < self.temple.get_map_height()):
            return True
        return False

    def _leads_to_wall(self, position: Position, direction):
        cell = _get_cell(position, direction, 2)
        return self.temple.is_wall(cell)

    def _navigate_to_new_cell(self, current_cell, available_directions):
        direction = self._choose_direction(available_directions)
        next_cell = self._carve_corridor(current_cell, direction)
        self._pending_cells.append(next_cell)
        self._last_direction = direction

    def _choose_direction(self, available_directions):
        if self._should_continue_in_last_direction(available_directions):
            return self._last_direction
        return self._choose_random_direction(available_directions)

    def _should_continue_in_last_direction(self, available_directions):
        """Determines if the last direction should be used again based on the "windy" probability."""
        return (self._last_direction in available_directions) and (random.random() > WINDING_PROBABILITY)

    def _choose_random_direction(self, available_directions):
        return random.choice(list(available_directions))

    def _carve_corridor(self, current_cell, direction):
        """Returns the next cell."""
        self._carve_corridor_by_direction(current_cell, direction, 1)
        return self._carve_corridor_by_direction(current_cell, direction, 2)

    def _carve_corridor_by_direction(self, current_cell, direction, step):
        cell = _get_cell(current_cell, direction, step)
        self.temple.carve(cell, Icon.CORRIDOR_FLOOR)
        return cell

    def _backtrack(self):
        self._pending_cells.pop()
        self._last_direction = None
