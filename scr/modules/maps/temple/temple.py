from ..tile import Tile
from ..grid import Grid
from ..map import Map
from .room import *
from .corridor import Corridor
from .connection import Connection
from .dead_end import DeadEnd
from .constants import BUILD_ROOM_ATTEMPTS, REGIONS_WALL_INDEX, ROOM_MIN_SIZE,MAX_MAP_WIDTH

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
        self.grid = Grid(Tile(Tile.WALL), width, height)

    def carve(self, position, tile):
        self.get_grid_cell(position).icon = tile
        self.regions.set(position, self.current_region_index)

    def is_wall(self, position: Position):
        tile = self.get_grid_cell(position)
        return tile.icon == Tile.WALL

    def is_floor(self, position: Position):
        tile = self.get_grid_cell(position)
        return tile.icon == Tile.CORRIDOR_FLOOR

    def is_door(self, position: Position):
        tile = self.get_grid_cell(position)
        return tile.icon == Tile.DOOR

    def increase_region_index(self):
        self.current_region_index += 1

    def get_grid_cell(self, position: Position):
        return self.grid.get(position)

    def _generate_level(self):
        self._add_rooms()
        self._fill_map_with_corridors()
        self._add_gateways()
        Connection(self).connect_regions()
        DeadEnd(self).remove_dead_ends()

    def _add_rooms(self):
        for i in range(BUILD_ROOM_ATTEMPTS):
            room = Room(self)
            if not room.is_intersect_with_other_rooms(self.rooms):
                self.rooms.append(room)

                self._place_room_on_map(room)
                self.increase_region_index()

    def _place_room_on_map(self, room):
        for x in range(room.upper_left_angle.x, room.bottom_right_angle.x):
            for y in range(room.upper_left_angle.y, room.bottom_right_angle.y):
                position = Position(x, y)
                self.carve(position, Tile.ROOM_FLOOR)

    def _fill_map_with_corridors(self):
        for x in range(1, self.grid.width, 2):
            for y in range(1, self.grid.height, 2):
                start_position = Position(x, y)
                self._process_corridor(start_position)

    def _process_corridor(self, start_position: Position):
        if not self.is_wall(start_position): return
        Corridor(self).generate_corridor(start_position)

    def _add_gateways(self):
        self.grid.get(ENTRANCE_POSITION).icon = Tile.ENTRANCE
        exit_position = Position(self.grid.width - 1, self.grid.height - 2)
        self.grid.get(exit_position).icon = Tile.EXIT
