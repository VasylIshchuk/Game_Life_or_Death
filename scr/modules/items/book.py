from ..core.game_entity import GameEntity


class Book(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self._effect: int = 0
        self._description: str = ""
        self._initialize_items_attributes()

    @property
    def effect(self) -> int:
        return self._effect
