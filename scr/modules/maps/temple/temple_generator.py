import random

from .floor import Floor
from .floor_creature_spawner import FloorCreatureSpawner
from .floor_item_spawner import FloorItemSpawner
from ...core.icons import Icon

MAIN_FLOOR_WIDTH = 43
MIN_FLOOR_HEIGHT = 41
INITIAL_LEVEL = 1


class TempleGenerator:
    def __init__(self, game_level):
        self._temple = []
        self._floors = game_level + 2
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
        self._place_key()

    def _generate_floor(self, number_floor):
        is_ground_floor = (number_floor == 0)
        floor_height = self._main_floor_width if is_ground_floor else self._get_floor_height(number_floor)

        floor = Floor(MAIN_FLOOR_WIDTH, floor_height, is_ground_floor)
        self._place_initial_entrance(floor, is_ground_floor)

        FloorCreatureSpawner(self._game_level, floor).spawn_creatures()
        FloorItemSpawner(floor).spawn_items()

        self._temple.append(floor)

    def _get_floor_height(self, number_floor):
        return self._main_floor_width - (number_floor * 10)

    def _place_key(self):
        floor = random.choice(self._temple)
        FloorItemSpawner(floor).place_chest_with_key()

    def _place_initial_entrance(self, floor, is_ground_floor):
        if self._is_initial_level() and is_ground_floor: floor.add_entrance(Icon.GRATE)

    def _is_initial_level(self):
        return self._game_level == INITIAL_LEVEL
