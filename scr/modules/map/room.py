import random
from position import Position
ROOM_MAX_SIZE = 9
ROOM_MIN_SIZE = 5


class Room:
    def __init__(self):
        self.upper_left_angle = Position(None,None)
        self.bottom_right_angle = Position(None,None)
        self.width = None
        self.height = None
        self._generate_room()

    def set_coordinates(self, x, y):
        self.upper_left_angle.x = x
        self.upper_left_angle.y = y
        self.bottom_right_angle.x = x + self.width
        self.bottom_right_angle.y = y + self.height

    def is_intersect_with_other_rooms(self, rooms):
        intersect = False
        for other_room in rooms:
            if self._intersect(other_room):
                intersect = True
                break
        return intersect

    def _intersect(self, other_room):
        """Returns True if this room intersects with another room."""
        return (self.upper_left_angle.x <= other_room.bottom_right_angle.x and self.bottom_right_angle.x >= other_room.upper_left_angle.x and
                self.upper_left_angle.y <= other_room.bottom_right_angle.y and self.bottom_right_angle.y >= other_room.upper_left_angle.y)

    def _generate_room(self):
        base_size = self._generate_base_size()
        rectangularity = self._generate_rectangularity(base_size)
        self._initialize_dimensions(base_size, rectangularity)


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

    def _initialize_dimensions(self, base_size, rectangularity):
        self.width = self._double_base_size(base_size)
        self.height = base_size
        self._randomly_apply_rectangularity(rectangularity)

    def _double_base_size(self, base_size):
        double_size = base_size * 2
        odd_double_size = double_size + 1
        return odd_double_size

    def _randomly_apply_rectangularity(self, rectangularity):
        if random.choice([True, False]):
            self.width += rectangularity
        elif rectangularity < ROOM_MIN_SIZE:
            self.height += rectangularity

    # def _validate_size_room(self):
    #     if self.width >=
