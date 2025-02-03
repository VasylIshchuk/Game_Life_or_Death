from ..core.game_entity import GameEntity


class Food(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.effect: int = 0
        self.initialize_items_attributes()
