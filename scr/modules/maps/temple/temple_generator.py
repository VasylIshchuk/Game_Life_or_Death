from .floor import Floor
from .floor_creature_spawner import FloorCreatureSpawner
from .floor_item_spawner import FloorItemSpawner

MAIN_FLOOR_WIDTH = 43
MIN_FLOOR_HEIGHT = 41


class TempleGenerator:
    def __init__(self, floor_count, game_level):
        self._temple = []
        self._floors = floor_count
        self._game_level = game_level
        self._main_floor_width = MIN_FLOOR_HEIGHT + (game_level * 10)
        self._generate_temple()

    def get_floor(self, number_floor):
        return self._temple[number_floor]

    def get_floor_count(self):
        return self._floors

    def _generate_temple(self):
        for number_floor in range(self._floors):
            self._generate_floor(number_floor)

    def _generate_floor(self, number_floor):
        is_ground_floor = (number_floor == 0)
        floor_height = self._main_floor_width if is_ground_floor else self._get_floor_height(number_floor)

        floor = Floor(MAIN_FLOOR_WIDTH, floor_height, is_ground_floor)
        FloorCreatureSpawner(self._game_level, floor)
        FloorItemSpawner(floor)

        self._temple.append(floor)

    def _get_floor_height(self, number_floor):
        return self._main_floor_width - (number_floor * 10)
