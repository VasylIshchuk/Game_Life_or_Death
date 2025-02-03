from ..core.game_entity import GameEntity


class Key(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.description: str = ""
        self.initialize_items_attributes()
