class EntitySpawner:
    def __init__(self, map):
        self._map = map

    def _spawn_creatures(self):
        for room in self._temple.rooms:
            self._handle_room(room)

    def _handle_room(self, room):
        for _ in range(self._generate_random_quantity_creatures()):
            self._add_creature(room)