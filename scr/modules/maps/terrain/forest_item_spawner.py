import random
from ..position import Position
from ...items.item_spawner import ItemSpawner

MIN_NUMBER_CHEST = 3
MAX_NUMBER_CHEST = 5


class ForestItemSwamper(ItemSpawner):
    def __init__(self, map):
        super().__init__(map)

    def spawn_creatures(self):
        for _ in range(self._generate_random_chest_quantity()):
            chest = self.generate_chest()
            self.initialize_chest(chest)
            self._place_chest(chest)

    def _generate_random_chest_quantity(self):
        return random.randint(MIN_NUMBER_CHEST, MAX_NUMBER_CHEST)

    def _place_chest(self, chest):
        position = self._generate_random_position()
        while not self._map.place_item(chest, position):
            position = self._generate_random_position()

    def _generate_random_position(self):
        x = random.randint(1, self._map.get_map_width() - 2)
        y = random.randint(1, self._map.get_map_height() - 2)
        return Position(x, y)
