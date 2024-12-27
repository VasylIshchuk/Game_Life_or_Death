from tile import Tile
from room import *
from corridor import Corridor
from position import Position

BUILD_ROOM_ATTEMPTS = 300
WALL_REGIONS_INDEX = -1
CORRIDOR_REGION_INDEX = 0


class Temple:
    def __init__(self):
        self.grid_level = []
        self.map_width = None
        self.map_height = None
        self.regions = []
        self.current_region_index = 1

    def generate_level(self, width, height):
        self._validate_odd_dimensions(width, height)
        self._initialize_map_attributes(width, height)
        self._initialize_initial_map()
        self._add_rooms()
        self._fill_map_with_corridors()

    def is_wall(self, x, y):
        return self.grid_level[x][y].icon == Tile.WALL

    def _validate_odd_dimensions(self, map_width, map_height):
        if map_width % 2 == 0 or map_height % 2 == 0:
            raise ValueError("Map dimensions must be odd-sized.")

    def _initialize_map_attributes(self, width, height):
        self.map_width = width
        self.map_height = height

    def _initialize_initial_map(self):
        self.regions = self._create_grid(WALL_REGIONS_INDEX)
        self.grid_level = self._create_grid(Tile(Tile.WALL))

    def _create_grid(self, default_value):
        grid = []
        for x in range(self.map_width):
            row = self._create_row(default_value)
            grid.append(row)
        return grid

    def _create_row(self, default_value):
        row = []
        for y in range(self.map_height):
            row.append(self._create_tile(default_value))
        return row

    def _create_tile(self, default_value):
        if isinstance(default_value, Tile):
            return Tile(default_value.icon)
        return default_value

    def _add_rooms(self):
        rooms = []
        for i in range(BUILD_ROOM_ATTEMPTS):
            room = self._generate_room()
            if not room.is_intersect_with_other_rooms(rooms):
                rooms.append(room)

                self._place_room_on_map(room)
                self._increase_region_index_for_next_room()

    def _generate_room(self):
        room = Room()
        x = self._generate_coordinate_for_room(self.map_width, room.width)
        y = self._generate_coordinate_for_room(self.map_height, room.height)
        room.set_coordinates(x, y)
        return room

    def _generate_coordinate_for_room(self, map_size, room_size):
        max_coordinate = map_size - room_size - 1
        random_coordinate = random.randint(0, max_coordinate) // 2
        odd_coordinate = random_coordinate * 2 + 1
        return odd_coordinate

    def _place_room_on_map(self, room):
        for x in range(room.upper_left_angle.x, room.bottom_right_angle.x):
            for y in range(room.upper_left_angle.y, room.bottom_right_angle.y):
                self.carve(x, y)

    def carve(self, x, y):
        self.grid_level[x][y].icon = Tile.FLOOR
        self.regions[x][y] = self.current_region_index

    def _increase_region_index_for_next_room(self):
        self.current_region_index += 1

    def _fill_map_with_corridors(self):
        self._set_corridor_region_index()
        for x in range(1, self.map_width, 2):
            for y in range(1, self.map_height, 2):
                if self.is_wall(x, y):
                    start_position = Position(x, y)
                    Corridor.generate_corridor(self, start_position)

    def _set_corridor_region_index(self):
        temple.current_region_index = CORRIDOR_REGION_INDEX

    def print_map(self):
        print('\n')
        for y in range(self.map_height):
            print(
                ''.join(str(self.grid_level[x][y].icon) for x in range(self.map_width)))
        print('\n')


temple = Temple()
temple.generate_level(191, 25)
temple.print_map()
