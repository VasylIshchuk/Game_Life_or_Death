from ..position import Position
from .region import Region


class GridPartitioner:
    def __init__(self, width, height):
        self._grid_width = width
        self._grid_height = height
        self.regions = []
        self._region_width = 0
        self._region_height = 0
        self._current_region_start_position = None
        self._current_region_end_position = None

    def get_regions(self):
        return self.regions

    def split_grid_into_regions(self, regions_quantity):
        self._generate_region_dimensions(regions_quantity)
        self._initialize_initial_region()
        for _ in range(regions_quantity):
            self._handle_region()

    def _generate_region_dimensions(self, regions_quantity):
        self._region_width =  (self._grid_width - 3) // regions_quantity
        self._region_height = (self._grid_height - 3) // regions_quantity

    def _initialize_initial_region(self):
        self._current_region_start_position = Position(1, 1)
        self._current_region_end_position = self._generate_position()
        self._add_new_region()

    def _generate_position(self):
        x = self._current_region_start_position.get_x() + self._region_width
        y = self._current_region_start_position.get_y() + self._region_height
        return Position(x, y)

    def _add_new_region(self):
        self.regions.append(self._get_region())

    def _handle_region(self):
        self._generate_region_position()
        self._add_new_region()

    def _generate_region_position(self):
        self._current_region_start_position = self._generate_position()
        self._current_region_end_position = self._generate_position()

    def _get_region(self):
        return Region( self._current_region_start_position, self._current_region_end_position)
