from ..position import Position
from ...core.icons import Icon
from ..direction import Direction, get_position_toward_direction


class DeadEnd:
    def __init__(self, map):
        self._map = map
        self.has_dead_end = None

    def remove_dead_ends(self):
        while True:
            self.has_dead_end = False
            self._handle_dead_ends()
            if not self.has_dead_end: break

    def _handle_dead_ends(self):
        for x in range(1, self._map.get_map_width()):
            for y in range(1, self._map.get_map_height()):
                position = Position(x, y)
                self._process_tile(position)

    def _process_tile(self, position):
        if not self._is_passable_tile(position): return
        connected_passable_tiles = self._get_connected_passable_tiles(position)
        if self._is_dead_end(connected_passable_tiles): self._remove_dead_end(position)

    def _is_passable_tile(self, position):
        return self._map.is_floor(position) or self._map.is_door(position)

    def _get_connected_passable_tiles(self, position):
        connected_passable_tiles = 0
        for direction in Direction.CARDINAL_DIRECTIONS:
            connected_tile_position = get_position_toward_direction(position, direction)
            if not self._map.is_wall(connected_tile_position):
                connected_passable_tiles += 1
        return connected_passable_tiles

    def _is_dead_end(self, connected_passable_tiles):
        return connected_passable_tiles < 2

    def _remove_dead_end(self, position):
        self._map.set_cell_icon(position, Icon.WALL)
        self.has_dead_end = True
