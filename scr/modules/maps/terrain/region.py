import random

from ..position import Position

class Region:

    def __init__(self, start_position, end_position):
        self.start_position = start_position
        self.end_position = end_position

    def get_start_position_x(self):
        return self.start_position.get_x()

    def get_start_position_y(self):
        return self.start_position.get_y()

    def get_end_position_x(self):
        return self.end_position.get_x()

    def get_end_position_y(self):
        return self.end_position.get_y()

    def generate_random_position(self):
        x = random.randint(self.get_start_position_x(),
                           self.get_end_position_x())
        y = random.randint(self.get_start_position_y(),
                           self.get_end_position_y())
        return Position(x, y)
