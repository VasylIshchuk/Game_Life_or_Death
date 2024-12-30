from .tile import Tile
from .position import Position


def create_cell(default_value):
    if isinstance(default_value, Tile):
        return Tile(default_value.icon)
    return default_value


class Grid:
    def __init__(self, default_value, width, height):
        self.width = width
        self.height = height
        self._grid = self._create_grid(default_value)

    def get(self, position: Position):
        return self._grid[position.x][position.y]

    def set(self, position: Position, value):
        self._grid[position.x][position.y] = value

    def _create_grid(self, default_value):
        grid = []
        for x in range(self.width):
            row = self._create_row(default_value)
            grid.append(row)
        return grid

    def _create_row(self, default_value):
        row = []
        for y in range(self.height):
            row.append(create_cell(default_value))
        return row
