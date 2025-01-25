from ..core.game_entity import GameEntity


class Artifact(GameEntity):

    def __init__(self, title):
        super().__init__(title)
        self.type: str = ""
        self.effect: int = 0
        self.durability: int = 0
        self.description: str = ""
        self._initialize_items_attributes()

    def is_usable(self):
        return self.durability > 0

    def decrease_durability(self, value):
        self.durability -= value
