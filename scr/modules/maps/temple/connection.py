import random
from math import sqrt

from ..position import Position
from ..tile import Tile
from ..grid import Grid
from .constants import DIRECTIONS, REGIONS_WALL_INDEX, ACCEPTABLE_DISTANCE, PROBABILITY_ADD_RANDOM_JUNCTION


class Connection:
    def __init__(self, temple):
        self.temple = temple
        self._connector_regions = Grid(None, self.temple.grid.width, self.temple.grid.height)
        self._connectors = set()
        self._merged_regions = {}
        self._open_regions = set()
        self._initialize_regions()

    def _initialize_regions(self):
        self._initialize_merged_regions(self.temple.current_region_index)
        self._initialize_open_regions(self.temple.current_region_index)

    def _initialize_merged_regions(self, current_region_index):
        for i in range(current_region_index + 1):
            self._merged_regions[i] = i

    def _initialize_open_regions(self, current_region_index):
        for i in range(current_region_index + 1):
            self._open_regions.add(i)

    def connect_regions(self):
        self._identify_connector_regions()
        self._create_connectors()
        self._merge_regions()

    def _identify_connector_regions(self):
        for x in range(1, self.temple.grid.width - 1):
            for y in range(1, self.temple.grid.height - 1):
                self._handle_tile(Position(x, y))

    def _handle_tile(self, position):
        if not self.temple.is_wall(position): return
        connected_regions = self._find_connected_regions(position)
        if not self._can_connected_regions(connected_regions): return
        self._connector_regions.set(position, connected_regions)

    def _find_connected_regions(self, wall_position):
        regions = set()
        for direction in DIRECTIONS:
            region = self._get_region_in_direction(wall_position, direction)
            if not self._is_wall_index(region):
                regions.add(region)
        return regions

    def _get_region_in_direction(self, position, direction):
        new_x = position.x + direction.x
        new_y = position.y + direction.y
        return self.temple.regions.get(Position(new_x, new_y))

    def _can_connected_regions(self, regions):
        return len(regions) > 1

    def _is_wall_index(self, region):
        return region == REGIONS_WALL_INDEX

    def _create_connectors(self):
        for x in range(0, self._connector_regions.width):
            for y in range(0, self._connector_regions.height):
                if self._connector_regions.get(Position(x, y)):
                    self._add_connector(x, y)

    def _add_connector(self, x, y):
        connector_position = Position(x, y)
        self._connectors.add(connector_position)

    def _merge_regions(self):
        while self._has_multiple_open_regions():
            connector = self._choose_random_connector()
            self._process_connector(connector)

    def _has_multiple_open_regions(self):
        return len(self._open_regions) > 2

    def _choose_random_connector(self):
        return random.choice(list(self._connectors))

    def _process_connector(self, connector):
        self._add_junction(connector)
        connected_regions = self._get_all_regions_connected_by_connector(connector)
        self._merge_connected_regions(connected_regions)
        self._clean_up_connectors(connector)

    def _add_junction(self, connector):
        tile = self.temple.grid.get(Position(connector.x, connector.y))
        tile.icon = Tile.DOOR

    def _get_all_regions_connected_by_connector(self, connector):
        regions = []
        for region_index in self._connector_regions.get(connector):
            index_connected_region = self._merged_regions[region_index]
            regions.append(index_connected_region)
        return regions

    def _merge_connected_regions(self, connected_regions):
        primary_region = connected_regions[0]
        regions_to_merge = connected_regions[1:]
        self._update_merged_regions(primary_region, regions_to_merge)
        self._close_merged_regions(regions_to_merge)

    def _update_merged_regions(self, primary_region, regions_to_merge):
        for i in range(self.temple.current_region_index + 1):
            if self._merged_regions[i] in regions_to_merge:
                self._merged_regions[i] = primary_region

    def _close_merged_regions(self, merged_regions):
        for region in merged_regions:
            self._open_regions.remove(region)

    def _clean_up_connectors(self, connector):
        connectors_to_remove = set()
        for connector_to_check in self._connectors:
            if self._is_within_proximity(connector, connector_to_check):
                connectors_to_remove.add(connector_to_check)
                continue
            if not self._has_multiple_connected_regions(connector_to_check):
                self._add_random_junction(connector_to_check)
                connectors_to_remove.add(connector_to_check)

        self._connectors.difference_update(connectors_to_remove)

    def _is_within_proximity(self, connector, connector_to_check):
        if self._calculate_distance(connector, connector_to_check) < ACCEPTABLE_DISTANCE:
            return True
        return False

    def _calculate_distance(self, current_position, target_position):
        return sqrt(pow(target_position.x - current_position.x, 2) + pow(target_position.y - current_position.y, 2))

    def _has_multiple_connected_regions(self, connector):
        regions = self.get_unique_regions_connected_by_connector(connector)
        if self._can_connected_regions(regions): return True
        return False

    def get_unique_regions_connected_by_connector(self, connector):
        regions = set()
        for region_index in self._connector_regions.get(connector):
            index_connected_region = self._merged_regions[region_index]
            regions.add(index_connected_region)
        return regions

    def _add_random_junction(self, connector):
        if random.random() < PROBABILITY_ADD_RANDOM_JUNCTION:
            self._add_junction(connector)
