from ..core.game_entity import GameEntity


class Key(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.description: str = ""
        self._level_number = None
        self.initialize_items_attributes()

    def set_level_number(self, level_number):
        self._level_number = level_number

    def get_level_number(self):
        return self._level_number
