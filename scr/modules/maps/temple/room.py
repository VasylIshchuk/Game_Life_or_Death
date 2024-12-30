import random
from ..position import Position
from .constants import ROOM_MAX_SIZE, ROOM_MIN_SIZE


class Room:
    def __init__(self, temple):
        self.temple = temple
        self.upper_left_angle = Position(None, None)
        self.bottom_right_angle = Position(None, None)
        self.width = None
        self.height = None
        self._generate_room()
        self._initialize_coordinates()

    def is_intersect_with_other_rooms(self, rooms):
        intersect = False
        for other_room in rooms:
            if self._intersect(other_room):
                intersect = True
                break
        return intersect

    def _intersect(self, other_room):
        """Returns True if this room intersects with another room."""
        return (
                self.upper_left_angle.x <= other_room.bottom_right_angle.x and self.bottom_right_angle.x >= other_room.upper_left_angle.x and
                self.upper_left_angle.y <= other_room.bottom_right_angle.y and self.bottom_right_angle.y >= other_room.upper_left_angle.y)

    def _generate_room(self):
        while True:
            base_size = self._generate_base_size()
            rectangularity = self._generate_rectangularity(base_size)
            self._initialize_dimensions(base_size, rectangularity)
            if self._validate_size_dimensions(): break

    def _generate_base_size(self):
        min_half = ROOM_MIN_SIZE // 2
        max_half = ROOM_MAX_SIZE // 2
        random_size = random.randint(min_half, max_half)
        odd_size = random_size * 2 + 1
        return odd_size

    def _generate_rectangularity(self, size):
        max_rectangularity = (size // 2) + 1
        random_rectangularity = random.randint(0, max_rectangularity)
        even_rectangularity = random_rectangularity * 2
        return even_rectangularity

    def _validate_size_dimensions(self):
        if self.width >= self.temple.grid.width or self.height >= self.temple.grid.height:
            return False
        return True

    def _initialize_dimensions(self, base_size, rectangularity):
        self.width = base_size
        self.height = base_size
        self._randomly_apply_rectangularity(rectangularity)

    def _randomly_apply_rectangularity(self, rectangularity):
        if random.choice([True, False]):
            self.width += rectangularity
        elif rectangularity < ROOM_MIN_SIZE:
            self.height += rectangularity

    def _initialize_coordinates(self):
        x = self._generate_coordinate_for_room(self.temple.grid.width, self.width)
        y = self._generate_coordinate_for_room(self.temple.grid.height, self.height)
        self._set_coordinates(x, y)

    def _generate_coordinate_for_room(self, map_size, room_size):
        max_coordinate = map_size - room_size - 1
        random_coordinate = random.randint(0, max_coordinate) // 2
        odd_coordinate = random_coordinate * 2 + 1
        return odd_coordinate

    def _set_coordinates(self, x, y):
        self.upper_left_angle.x = x
        self.upper_left_angle.y = y
        self.bottom_right_angle.x = x + self.width
        self.bottom_right_angle.y = y + self.height
