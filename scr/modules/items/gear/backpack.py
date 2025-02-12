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

    def remove_item_from_backpack(self, index):
        if not self.slot_has_item: return False

        for i in range(index, self.current_size - 1):
            self.slots[i] = self.slots[i + 1]

        self.slots[self.current_size - 1] = None
        self.current_size -= 1
        return True

