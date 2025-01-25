from ..core.game_entity import GameEntity


class Weapon(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self._type: str = ""
        self._durability: int = 0
        self._strike_power: int = 0
        self._strike_distance: int = 0
        self._initialize_items_attributes()

    @property
    def type(self) -> str:
        return self._type

    @property
    def durability(self) -> int:
        return self._durability

    @property
    def strike_power(self) -> int:
        return self._strike_power

    @property
    def strike_distance(self) -> int:
        return self._strike_distance

    def decrease_durability(self, value):
        self._durability -= value

    def is_broken(self):
        return self._durability <= 0
