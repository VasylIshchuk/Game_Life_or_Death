from ..core.game_entity import GameEntity


class Armor(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self._defense: int = 0
        self.initialize_items_attributes()

    def update_defence(self, value):
        self._defense = value

    def get_defence_effect(self):
        return self._defense

    def is_usable(self):
        return self._defense > 0
