import random

from ..position import Position
from ...core.icons import Icon

NEIGHBOR_OFFSETS = [-1, 0, 1]

ICONS = [Icon.WATER, Icon.SWAMP, Icon.STONE]

SPREAD_CHANCES = {
    Icon.STONE: 0.1,
    Icon.WATER: 0.2,
    Icon.SWAMP: 0.25,
}

DENSITIES = {
    Icon.STONE: 0.05,
    Icon.WATER: 0.01,
    Icon.SWAMP: 0.01,
}


class TerrainElementPlacer:
    def __init__(self, game_map):
        self._map = game_map
        self._height = self._map.get_map_height()
        self._width = self._map.get_map_width()

    def populate_map_with_elements(self):
        for icon in ICONS:
            self._generate_cluster_growth(icon)

    def _generate_cluster_growth(self, icon):
        self._place_random_tiles(icon, DENSITIES[icon])
        self._spread_clusters(icon)

    def _place_random_tiles(self, icon, density):
        quantity = self._calculate_quantity(density)
        for _ in range(quantity):
            position = self._generate_random_position()
            self._map.set_cell_icon(position, icon)

    def _calculate_quantity(self, density):
        return int(self._height * self._width * density)

    def _generate_random_position(self):
        x = random.randint(1, self._width - 2)
        y = random.randint(1, self._height - 2)
        return Position(x, y)

    def _spread_clusters(self, icon):
        for x in range(self._width):
            for y in range(self._height):
                position = Position(x, y)
                self._handle_cluster(position, icon)

    def _handle_cluster(self, position, icon):
        if self._is_cluster(position, icon):
            self._spread_to_neighbors(position, icon)

    def _is_cluster(self, position, icon):
        return self._map.get_cell_icon(position) == icon

    def _spread_to_neighbors(self, position, icon):
        for dx in NEIGHBOR_OFFSETS:
            for dy in NEIGHBOR_OFFSETS:
                neighbor_position = Position(position.x + dx, position.y + dy)
                self._handel_neighbor(neighbor_position, icon)

    def _handel_neighbor(self, position, icon):
        if self._is_valid_spread_target(position, icon):
            self._map.set_cell_icon(position, icon)

    def _is_valid_spread_target(self, position, icon):
        return self._is_within_bounds(position) and self._can_spread_to(position, icon)

    def _is_within_bounds(self, position):
        return 0 < position.get_x() < self._width - 1 and 0 < position.get_y() < self._height - 1

    def _can_spread_to(self, position, icon):
        return self._map.get_cell_icon(position) == Icon.TREE and random.random() < SPREAD_CHANCES[icon]
