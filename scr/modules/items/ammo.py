from ..core.game_entity import GameEntity


class Ammo(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.quantity: int = 0
        self.initialize_items_attributes()

    def is_usable(self):
        return self.quantity > 0

    def decrease_quantity(self):
        self.quantity -= 1

