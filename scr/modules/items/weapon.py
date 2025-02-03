from ..core.game_entity import GameEntity


class Weapon(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.type: str = ""
        self.durability: int = 0
        self.strike_power: int = 0
        self.strike_distance: int = 0
        self.initialize_items_attributes()

    def decrease_durability(self, value):
        self.durability -= value

    def is_broken(self):
        return self.durability <= 0
