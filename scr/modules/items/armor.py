from ..core.game_entity import GameEntity


class Armor(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self._defense: int = 0
        self.initialize_items_attributes()
