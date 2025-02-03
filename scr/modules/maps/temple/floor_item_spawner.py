import random
from ..position import Position
from ...items.item_spawner import ItemSpawner

MIN_CHEST_COUNT = 1
MAX_CHEST_COUNT = 2
ONE_CHEST_SPAWN_PROBABILITY = 0.4
TWO_CHEST_SPAWN_PROBABILITY = 0.2
NO_CHESTS = 0


class FloorItemSpawner(ItemSpawner):
    def __init__(self, map):
        super().__init__(map)
        self._spawn_items()

    def _spawn_items(self):
        for room in self._map.rooms:
            self._handle_room(room)

    def _handle_room(self, room):
        for _ in range(self._generate_random_chest_quantity()):
            chest = self.generate_chest()
            self._place_chest_in_room(chest, room)

    def _generate_random_chest_quantity(self):
        if random.random() < TWO_CHEST_SPAWN_PROBABILITY:
            return 2
        elif random.random() < ONE_CHEST_SPAWN_PROBABILITY:
            return 1
        return 0

    def _place_chest_in_room(self, chest, room):
        max_attempts = 5
        for _ in range(max_attempts):
            position = self._generate_random_position(room)
            if self._map.place_item(chest, position):
                return

    def _generate_random_position(self, room):
        x = random.randint(room.get_x_upper_left_angle() + 2, room.get_x_bottom_right_angle() - 2)
        y = random.randint(room.get_y_upper_left_angle() + 2, room.get_y_bottom_right_angle() - 2)
        return Position(x, y)
