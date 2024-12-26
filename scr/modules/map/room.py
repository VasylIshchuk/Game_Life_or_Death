import random

ROOM_MAX_SIZE = 9
ROOM_MIN_SIZE = 5


class Room:
    def __init__(self):
        self.x_upper_left = None
        self.y_upper_left = None
        self.x_bottom_right = None
        self.y_bottom_right = None
        self.width = None
        self.height = None
        self._generate_room()

    def set_coordinates(self, x, y):
        """Sets the coordinates of the room based in the top-left corner (x, y)."""
        self.x_upper_left = x
        self.y_upper_left = y
        self.x_bottom_right = x + self.width
        self.y_bottom_right = y + self.height

    def is_intersect_with_other_rooms(self, rooms):
        """Checks if this room intersects with any other rooms."""
        intersect = False
        for other_room in rooms:
            if self._intersect(other_room):
                intersect = True
                break
        return intersect

    def _intersect(self, other_room):
        """Returns True if this room intersects with another room."""
        return (self.x_upper_left <= other_room.x_bottom_right and self.x_bottom_right >= other_room.x_upper_left and
                self.y_upper_left <= other_room.y_bottom_right and self.y_bottom_right >= other_room.y_upper_left)

    def _generate_room(self):
        base_size = self._generate_base_size()
        rectangularity = self._generate_rectangularity(base_size)
        self._initialize_dimensions(base_size, rectangularity)

    def _generate_base_size(self):
        """Generates the base size of the room, ensuring it's odd."""
        min_half = ROOM_MIN_SIZE // 2
        max_half = ROOM_MAX_SIZE // 2
        return random.randint(min_half, max_half) * 2 + 1

    def _generate_rectangularity(self, size):
        """Generates the amount of rectangularity to add to the room."""
        max_rectangularity = (size // 2) + 1
        return random.randint(0, max_rectangularity) * 2

    def _initialize_dimensions(self, base_size, rectangularity):
        """Initializes the width and height of the room based on the base size and applies rectangularity."""
        self.width = base_size * 2 + 1
        self.height = base_size
        self._apply_rectangularity(rectangularity)

    def _apply_rectangularity(self, rectangularity):
        """Randomly applies rectangularity to either the width or height."""
        if random.choice([True, False]):
            self.width += rectangularity
        elif rectangularity < ROOM_MIN_SIZE:
            self.height += rectangularity
