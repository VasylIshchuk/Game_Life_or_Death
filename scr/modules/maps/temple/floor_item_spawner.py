import random
from ..position import Position
from ...items.item_spawner import ItemSpawner
from ...items.item_factory import ItemFactory

ONE_CHEST_SPAWN_PROBABILITY = 0.4
TWO_CHEST_SPAWN_PROBABILITY = 0.2


class FloorItemSpawner(ItemSpawner):
    def __init__(self, map):
        super().__init__(map)

    def place_chest_with_key(self):
        chest = self.generate_chest()
        self._put_key_in_chest(chest)
        room = random.choice(self._map.rooms)
        self.place_item_in_room(chest, room)

    def _put_key_in_chest(self, chest):
        key = ItemFactory().create_item("Key")
        chest.slots[0] = key

    def spawn_items(self):
        for room in self._map.rooms:
            self._handle_room(room)

    def _handle_room(self, room):
        for _ in range(self._generate_random_chest_quantity()):
            chest = self.generate_chest()
            self.initialize_chest(chest)
            self.place_item_in_room(chest, room)

    def _generate_random_chest_quantity(self):
        if random.random() < TWO_CHEST_SPAWN_PROBABILITY:
            return 2
        elif random.random() < ONE_CHEST_SPAWN_PROBABILITY:
            return 1
        return 0

    def place_item_in_room(self, item, room):
        position = self._generate_random_position(room)
        while not self._map.place_item(item, position):
            position = self._generate_random_position(room)

    def _generate_random_position(self, room):
        x = random.randint(room.get_x_upper_left_angle() + 2, room.get_x_bottom_right_angle() - 2)
        y = random.randint(room.get_y_upper_left_angle() + 2, room.get_y_bottom_right_angle() - 2)
        return Position(x, y)
