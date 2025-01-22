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

    def get_x_upper_left_angle(self):
        return self.upper_left_angle.get_x()

    def get_y_upper_left_angle(self):
        return self.upper_left_angle.get_y()

    def get_x_bottom_right_angle(self):
        return self.bottom_right_angle.get_x()

    def get_y_bottom_right_angle(self):
        return self.bottom_right_angle.get_y()

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
                self.upper_left_angle.get_x() <= other_room.bottom_right_angle.get_x() and
                self.bottom_right_angle.get_x() >= other_room.upper_left_angle.get_x() and
                self.upper_left_angle.get_y() <= other_room.bottom_right_angle.get_y() and
                self.bottom_right_angle.get_y() >= other_room.upper_left_angle.get_y())

    def set_coordinates(self, coordinate):
        self.upper_left_angle = coordinate
        self._set_bottom_right_angle(coordinate)

    def _set_bottom_right_angle(self, coordinate):
        x = coordinate.get_x() + self.width
        y = coordinate.get_y() + self.height
        position = Position(x, y)
        self.bottom_right_angle = position

    def generate_room(self):
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
        if self.width >= self.temple.get_map_width() or self.height >= self.temple.get_map_height():
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
