class Inventory:

    def __init__(self, size):
        self.size = size
        self.slots = [None] * size

    def get_item(self, index):
        return self.slots[index]

    def delete_item(self, index):
        if not self._slot_has_item: return False
        self.slots[index] = None
        return True

    def _slot_has_item(self, index):
        return self.slots[index] is not None
