from ..position import Position
from ..tile import Tile
from .constants import DIRECTIONS


class DeadEnd:
    def __init__(self, temple):
        self.temple = temple
        self.has_dead_end = None

    def remove_dead_ends(self):
        while True:
            self.has_dead_end = False
            self._handle_dead_ends()
            if not self.has_dead_end: break

    def _handle_dead_ends(self):
        for x in range(1, self.temple.grid.width):
            for y in range(1, self.temple.grid.height):
                self._process_tile(Position(x, y))

    def _process_tile(self, position):
        if not self.temple.is_floor(position) and not self.temple.is_door(position): return
        connected_passable_tiles = self._get_connected_passable_tiles(position)
        if not self._is_dead_end(connected_passable_tiles): return
        self.temple.get_grid_cell(position).icon = Tile.WALL
        self.has_dead_end = True

    def _get_connected_passable_tiles(self, position):
        connected_passable_tiles = 0
        for direction in DIRECTIONS:
            connected_tile_position = Position(position.x + direction.x, position.y + direction.y)
            if not self.temple.is_wall(connected_tile_position):
                connected_passable_tiles += 1
        return connected_passable_tiles

    def _is_dead_end(self, connected_passable_tiles):
        return connected_passable_tiles < 2
