from .forest import Forest
from .forest_creature_spawner import ForestCreatureSpawner
from .forest_item_spawner import ForestItemSwamper

MAIN_FLOOR_WIDTH = 43
MIN_FLOOR_HEIGHT = 41


class TerrainGenerator:
    def generate_terrain(self, game_level):
        height = self._get_floor_height(game_level)
        forest = Forest(MAIN_FLOOR_WIDTH, height)
        ForestCreatureSpawner(game_level, forest).spawn_creatures()
        ForestItemSwamper(forest).spawn_items()
        return forest

    def _get_floor_height(self, game_level):
        return MIN_FLOOR_HEIGHT + (game_level * 20)
