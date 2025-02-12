import random

from .temple import Temple
from .floor_creature_spawner import FloorCreatureSpawner
from .floor_item_spawner import FloorItemSpawner


def _place_key(temple, level_number):
    floor = random.choice(temple.floors)
    FloorItemSpawner(floor).place_chest_with_key(level_number)


class TempleGenerator:
    @staticmethod
    def generate_temple(level_number):
        temple = Temple(level_number)
        for floor in temple.floors:
            FloorCreatureSpawner(level_number, floor).spawn_creatures()
            FloorItemSpawner(floor).spawn_items()
        _place_key(temple, level_number)
        return temple
