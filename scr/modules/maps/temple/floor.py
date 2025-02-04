from ...core.icons import Icon
from ..grid import Grid
from ..map import Map
from .room import *
from .corridor import Corridor
from .connection import Connection
from .dead_end import DeadEnd
from .constants import BUILD_ROOM_ATTEMPTS, REGIONS_WALL_INDEX, ROOM_MIN_SIZE

ENTRANCE_POSITION = Position(0, 1)


class Floor(Map):
    def __init__(self, width, height, is_ground_floor=False):
        super().__init__()
        self.is_ground_floor = is_ground_floor
        self.regions = None
        self.rooms = []
        self.current_region_index = 0
        self._validate_dimensions(width, height)
        self.regions = Grid(REGIONS_WALL_INDEX, width, height)
        self._initialize_initial_grid(width, height)
        self._generate_floor()

    def is_wall(self, position: Position):
        return self.get_cell_icon(position) == Icon.WALL

    def is_floor(self, position: Position):
        return self.get_cell_icon(position) == Icon.CORRIDOR_FLOOR

    def is_door(self, position: Position):
        return self.get_cell_icon(position) == Icon.DOOR

    def carve(self, position, icon):
        self.set_cell_icon(position, icon)
        self.regions.set_value(position, self.current_region_index)

    def increase_region_index(self):
        self.current_region_index += 1

    def get_current_region_index(self):
        return self.current_region_index

    def _validate_dimensions(self, width, height):
        self._validate_min_size_dimensions(width, height)
        self._validate_odd_dimensions(width, height)

    def _validate_min_size_dimensions(self, width, height):
        if width <= ROOM_MIN_SIZE or height <= ROOM_MIN_SIZE:
            raise ValueError(f"Map dimensions must be larger than [{ROOM_MIN_SIZE}:{ROOM_MIN_SIZE}]")

    def _validate_odd_dimensions(self, width, height):
        if width % 2 == 0 or height % 2 == 0:
            raise ValueError("Map dimensions must be odd-sized.")

    def _initialize_initial_grid(self, width, height):
        self.regions = Grid(REGIONS_WALL_INDEX, width, height)
        self.initialize_grid(Icon.WALL, width, height)

    def _generate_floor(self):
        self._add_rooms()
        self._fill_map_with_corridors()
        self._add_gateways()
        Connection(self).connect_regions()
        DeadEnd(self).remove_dead_ends()

    def _add_rooms(self):
        for i in range(BUILD_ROOM_ATTEMPTS):
            self._handle_room()

    def _handle_room(self):
        room = self._create_room()

        coordinate_room = self._generate_coordinates(room)
        room.set_coordinates(coordinate_room)

        if not room.is_intersect_with_other_rooms(self.rooms):
            self._add_room_to_map(room)
            self.increase_region_index()

    def _create_room(self):
        room = Room(self)
        room.generate_room()
        return room

    def _generate_coordinates(self, room):
        x = self._generate_coordinate_for_room(self.get_map_width(), room.width)
        y = self._generate_coordinate_for_room(self.get_map_height(), room.height)
        return Position(x, y)

    def _generate_coordinate_for_room(self, map_size, room_size):
        max_coordinate = map_size - room_size - 1
        random_coordinate = random.randint(0, max_coordinate) // 2
        odd_coordinate = random_coordinate * 2 + 1
        return odd_coordinate

    def _add_room_to_map(self, room):
        self.rooms.append(room)
        self._place_room_on_map(room)

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
        if self.is_ground_floor:
            self._add_entrance()
            self._add_exit()

        self._add_stairs()

    def _add_entrance(self):
        self.set_cell_icon(ENTRANCE_POSITION, Icon.GATEWAY)

    def _add_exit(self):
        exit_position = Position(self.get_map_width() - 1, self.get_map_height() - 2)
        self.set_cell_icon(exit_position, Icon.GATEWAY)

    def _add_stairs(self):
        mid_height = self._make_odd(self.get_map_height() // 2)
        position_down = Position(0, mid_height)
        self.set_cell_icon(position_down, Icon.STAIRS)

    def _make_odd(self, value):
        return value if value % 2 == 1 else value + 1

