from ..inventory import Inventory


class Backpack(Inventory):
    def __init__(self, size=15):
        super().__init__(size)
        self.current_size = 0

    def add_item(self, item):
        if self._is_slots_full(): return False
        self.slots[self.current_size] = item
        self.current_size += 1
        return True

    def _is_slots_full(self):
        return self.current_size == self.size

    def delete_item(self, index):
        super().delete_item(index)
        self.current_size -= 1
