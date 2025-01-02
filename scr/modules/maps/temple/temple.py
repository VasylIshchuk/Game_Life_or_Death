from ...core.icons import Icon
from ..tile import Tile
from ..grid import Grid
from ..map import Map
from .room import *
from .corridor import Corridor
from .connection import Connection
from .dead_end import DeadEnd
from .constants import BUILD_ROOM_ATTEMPTS, REGIONS_WALL_INDEX, ROOM_MIN_SIZE, MAX_MAP_WIDTH

ENTRANCE_POSITION = Position(0, 1)


class Temple(Map):
    def __init__(self, width, height):
        super().__init__()
        self.regions = None
        self.rooms = []
        self.current_region_index = 0
        self._validate_dimensions(width, height)
        self._initialize_initial_grid(width, height)
        self._generate_level()

    def carve(self, position, icon):
        self.set_cell_icon(position, icon)
        self.regions.set_value(position, self.current_region_index)

    def increase_region_index(self):
        self.current_region_index += 1

    def get_current_region_index(self):
        return self.current_region_index

    def _validate_dimensions(self, width, height):
        self._validate_min_size_dimensions(width, height)
        self._validate_max_width_dimensions(width)
        self._validate_odd_dimensions(width, height)

    def _validate_min_size_dimensions(self, width, height):
        if width <= ROOM_MIN_SIZE or height <= ROOM_MIN_SIZE:
            raise ValueError(f"Map dimensions must be larger than [{ROOM_MIN_SIZE}:{ROOM_MIN_SIZE}]")

    def _validate_max_width_dimensions(self, width):
        if width > MAX_MAP_WIDTH:
            raise ValueError(f"Map width must not exceed [{MAX_MAP_WIDTH}]")

    def _validate_odd_dimensions(self, width, height):
        if width % 2 == 0 or height % 2 == 0:
            raise ValueError("Map dimensions must be odd-sized.")

    def _initialize_initial_grid(self, width, height):
        self.regions = Grid(REGIONS_WALL_INDEX, width, height)
        tile_wall = Tile(Icon.WALL)
        self.grid = Grid(tile_wall, width, height)

    def _generate_level(self):
        self._add_rooms()
        self._fill_map_with_corridors()
        self._add_gateways()
        Connection(self).connect_regions()
        DeadEnd(self).remove_dead_ends()

    def _add_rooms(self):
        for i in range(BUILD_ROOM_ATTEMPTS):
            self._handle_room()

    def _handle_room(self):
        room = Room(self)
        if not room.is_intersect_with_other_rooms(self.rooms):
            self.rooms.append(room)

            self._place_room_on_map(room)
            self.increase_region_index()

    def _place_room_on_map(self, room):
        for x in range(room.get_x_upper_left_angle(), room.get_x_bottom_right_angle()):
            for y in range(room.get_y_upper_left_angle(), room.get_y_bottom_right_angle()):
                position = Position(x, y)
                self.carve(position, Icon.ROOM_FLOOR)

    def _fill_map_with_corridors(self):
        for x in range(1, self.grid.get_width(), 2):
            for y in range(1, self.grid.get_height(), 2):
                start_position = Position(x, y)
                self._handle_corridor(start_position)

    def _handle_corridor(self, start_position: Position):
        if not self.is_wall(start_position): return
        Corridor(self).generate_corridor(start_position)

    def _add_gateways(self):
        self.set_cell_icon(ENTRANCE_POSITION, Icon.ENTRANCE)
        exit_position = Position(self.grid.width - 1, self.grid.height - 2)
        self.set_cell_icon(exit_position, Icon.EXIT)
