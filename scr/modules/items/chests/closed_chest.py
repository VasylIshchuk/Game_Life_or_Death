from ..chest import Chest


class ClosedChest(Chest):
    def __init__(self, title):
        super().__init__(title)
        self.initialize_items_attributes()
