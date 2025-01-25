from ...core.game_entity import GameEntity

class Artifact(GameEntity):

    def __init__(self, title):
        super().__init__(title)
        self._type: str = ""
        self._effect: int = 0
        self._durability: int = 0
        self._description: str = ""
        self._initialize_items_attributes()

    def is_usable(self):
        return self.durability > 0

    @property
    def durability(self) -> int:
        return self._durability

    @property
    def type(self) -> str:
        return self._type

    @property
    def effect(self) -> int:
        return self._effect

    def decrease_durability(self,value):
        self._durability -= value


