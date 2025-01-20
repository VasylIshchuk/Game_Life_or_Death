from .terrain_element_placer import TerrainElementPlacer
from .grid_partitioner import GridPartitioner
from .region_generator import RegionGenerator
from .region_connector import RegionConnector
from ..map import Map
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
        region_connector = RegionConnector(self, self._start_position_regions)
        region_connector.connect_regions(REGIONS_QUANTITY)
