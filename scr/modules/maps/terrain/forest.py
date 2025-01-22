from .terrain_element_placer import TerrainElementPlacer
from .grid_partitioner import GridPartitioner
from .region_generator import RegionGenerator
from .region_connector import Connector
from ..map import Map
from ..position import Position
from ...core.icons import Icon

REGIONS_QUANTITY = 4


class Forest(Map):
    def __init__(self, width, height):
        super().__init__()
        self.initialize_grid(Icon.TREE, width, height)
        self._regions_position = []
        self._start_position_regions = []
        self._generate_level()

    def _generate_level(self):
        TerrainElementPlacer(self).populate_map_with_elements()
        self._create_regions()
        self._connect_regions()
        self._handle_gateways()

    def _create_regions(self):
        self._regions_position = self._generate_regions_position()
        for idx_region in range(REGIONS_QUANTITY):
            start_position = self._generate_random_position_in_region(idx_region)
            self._start_position_regions.append(start_position)
            RegionGenerator(self).generate_region(start_position)

    def _generate_regions_position(self):
        grid_partitioner = GridPartitioner(self.get_map_width(), self.get_map_height())
        grid_partitioner.split_grid_into_regions(REGIONS_QUANTITY)
        return grid_partitioner.get_regions()

    def _generate_random_position_in_region(self, idx_region):
        return self._regions_position[idx_region].generate_random_position()

    def _connect_regions(self):
        region_connector = Connector(self)
        region_connector.connect_regions(REGIONS_QUANTITY, self._start_position_regions)

    def _handle_gateways(self):
        exit_position = Position(self.get_map_height() - 1, self.get_map_height() - 2)
        entrance_position = Position(0, 1)

        self._add_gateways(entrance_position, exit_position)
        self._connect_gateways(entrance_position, exit_position)

    def _add_gateways(self, entrance_position, exit_position):
        self._add_entrance(entrance_position)
        self._add_exit(exit_position)

    def _add_entrance(self, position):
        self.set_cell_icon(position, Icon.GATEWAY)

    def _add_exit(self, position):
        self.set_cell_icon(position, Icon.LEVEL_EXIT)

    def _connect_gateways(self, entrance_position, exit_position):
        connector = Connector(self)
        connector.connect_gateway(exit_position)
        connector.connect_gateway(entrance_position)
