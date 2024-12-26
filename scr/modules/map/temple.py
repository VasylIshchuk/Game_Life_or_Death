import random

from tile import Tile
from room import Room

BUILD_ROOM_ATTEMPTS = 500


class Temple:
    def __init__(self):
        self.grid_level = []
        self.map_width = None
        self.map_height = None
        self._regions = []
        self._current_region = 1

    def generate_level(self, width, height):
        """Generates a temple level with given dimensions."""
        self._validate_odd_dimensions(width, height)
        self._initialize_map_attributes(width, height)
        self._initialize_initial_map()
        self._add_rooms()

    def _validate_odd_dimensions(self, map_width, map_height):
        """Validates that the map dimensions are odd numbers."""
        if map_width % 2 == 0 or map_height % 2 == 0:
            raise ValueError("Map dimensions must be odd-sized.")

    def _initialize_map_attributes(self, width, height):
        """Initializes basic map attributes such as width and height."""
        self.map_width = width
        self.map_height = height

    def _initialize_initial_map(self):
        """Sets up the initial map grid and regions with default values."""
        self._regions = self._create_grid(-1)
        self.grid_level = self._create_grid(Tile.WALL)

    def _create_grid(self, default_value):
        """Creates a 2D grid filled with a default value."""
        grid = []
        for x in range(self.map_width):
            row = []
            for y in range(self.map_height):
                row.append(default_value)
            grid.append(row)
        return grid

    def _add_rooms(self):
        """Attempts to add rooms to the map without overlap."""
        rooms = []
        for i in range(BUILD_ROOM_ATTEMPTS):
            room = self._generate_room()
            if not room.is_intersect_with_other_rooms(rooms):
                rooms.append(room)

                self._place_room_on_map(room)
                self._increase_region()

    def _generate_room(self):
        """Generates a room with random coordinates."""
        room = Room()
        x = self._generate_coordinate(self.map_width, room.width)
        y = self._generate_coordinate(self.map_height, room.height)
        room.set_coordinates(x, y)
        return room

    def _generate_coordinate(self, map_size, room_size):
        """Generates a random coordinate ensuring the room fits within bounds.
            The coordinate is adjusted to always be odd for proper alignment."""
        max_coordinate = map_size - room_size - 1
        return (random.randint(0, max_coordinate) // 2) * 2 + 1

    def _place_room_on_map(self, room):
        """Places the room on the map by carving out floor tiles."""
        for x in range(room.x_upper_left, room.x_bottom_right):
            for y in range(room.y_upper_left, room.y_bottom_right):
                self._carve(x, y)

    def _carve(self, x, y):
        """Carves out a floor tile at the given coordinates."""
        self.grid_level[x][y] = Tile.FLOOR
        self._regions[x][y] = self._current_region

    def _increase_region(self):
        """Increments the region counter for the next room."""
        self._current_region += 1

    def print_map(self):
        print('\n')
        for y in range(self.map_height):
            print(
                ''.join(str(self.grid_level[x][y]) for x in range(self.map_width)))
        print('\n')


temple = Temple()
temple.generate_level(171, 41)
temple.print_map()
