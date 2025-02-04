import random
from ..position import Position
from ...items.item_spawner import ItemSpawner
from ..direction import Direction

MIN_NUMBER_CHEST = 3
MAX_NUMBER_CHEST = 5


class ForestItemSwamper(ItemSpawner):
    def __init__(self, map):
        super().__init__(map)

    def spawn_items(self):
        for _ in range(self._generate_random_chest_quantity()):
            chest = self.generate_chest()
            self.initialize_chest(chest)
            self.place_item_in_forest(chest)

    def _generate_random_chest_quantity(self):
        return random.randint(MIN_NUMBER_CHEST, MAX_NUMBER_CHEST)

    def place_item_in_forest(self, item):
        while True:
            position = self._generate_random_position()
            if not self._validate_position(position): continue
            self._map.place_item(item, position)
            break

    def _generate_random_position(self):
        x = random.randint(1, self._map.get_map_width() - 2)
        y = random.randint(1, self._map.get_map_height() - 2)
        return Position(x, y)

    def _validate_position(self, position):
        if not self._map.is_ground(position): return False;

        for direction in Direction.COMPASS_DIRECTIONS:
            tile_in_direction = self._get_tile_in_direction(position, direction)
            if not self._map.is_ground(tile_in_direction): return False;
        return True

    def _get_tile_in_direction(self, position, direction):
        x = position.get_x() + direction.get_x()
        y = position.get_y() + direction.get_y()
        return Position(x, y)
