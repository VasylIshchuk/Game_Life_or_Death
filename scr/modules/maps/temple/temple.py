from .floor import Floor
from ...core.icons import Icon

MAIN_FLOOR_WIDTH = 51
MIN_FLOOR_HEIGHT = 41
INITIAL_LEVEL = 1


class Temple:
    def __init__(self, level_number):
        self.floors = []
        self.floor_count = level_number + 2
        self.level_number = level_number
        self.main_floor_width = MIN_FLOOR_HEIGHT + (level_number * 10)
        self._generate_temple()

    def get_floor(self, number_floor):
        return self.floors[number_floor]

    def get_total_floors(self):
        return self.floor_count

    def _generate_temple(self):
        for number_floor in range(self.floor_count):
            self._generate_floor(number_floor)

    def _generate_floor(self, number_floor):
        is_ground_floor = (number_floor == 0)
        floor_height = self.main_floor_width if is_ground_floor else self._calculate_floor_height(number_floor)

        floor = Floor(MAIN_FLOOR_WIDTH, floor_height, is_ground_floor)
        self._place_initial_entrance(floor, is_ground_floor)

        self.floors.append(floor)

    def _calculate_floor_height(self, number_floor):
        return self.main_floor_width - (number_floor * 10)

    def _place_initial_entrance(self, floor, is_ground_floor):
        if self._is_initial_level() and is_ground_floor: floor.add_entrance(Icon.GRATE)

    def _is_initial_level(self):
        return self.level_number == INITIAL_LEVEL
