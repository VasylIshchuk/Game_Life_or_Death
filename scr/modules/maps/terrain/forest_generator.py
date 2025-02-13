from .forest import Forest
from .forest_creature_spawner import ForestCreatureSpawner
from .forest_item_spawner import ForestItemSwamper

MAIN_FLOOR_WIDTH = 41
MIN_FLOOR_HEIGHT = 31


def _calculate_forest_height(level_number):
    return MIN_FLOOR_HEIGHT + (level_number * 20)


class ForestGenerator:
    @staticmethod
    def generate_forest(level_number):
        height = _calculate_forest_height(level_number)
        forest = Forest(MAIN_FLOOR_WIDTH, height)
        ForestCreatureSpawner(level_number, forest).spawn_creatures()
        ForestItemSwamper(forest).spawn_items()
        return forest
