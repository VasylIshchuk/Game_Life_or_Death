import random

from ..core.game_entity import GameEntity

MIN_SIZE = 1
MAX_SIZE = 4


def generate_size():
    return random.randint(MIN_SIZE, MAX_SIZE)


class Chest(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.size = generate_size()
        self._slots = [None] * self.size

    def remove_item(self, item):
        self._slots.remove(item)

    def get_slots(self):
        return self._slots

    def get_item(self, index):
        return self._slots[index]

    def set_item(self, index, item):
        self._slots[index] = item

    def is_empty(self):
        return len(self._slots) == 0

    def put_item(self, item):
        if self._is_slots_full(): return False
        self._slots.append(item)
        return True

    def _is_slots_full(self):
        return self.size == len(self._slots)
