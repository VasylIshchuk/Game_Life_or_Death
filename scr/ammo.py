from item import Item
from game_entity import _load_data_from_file, _parse_attribute


class Ammo(Item):
    def __init__(self, title):
        super().__init__(title)

        data_ammo = _load_data_from_file("../items.json", title)
        self.category = _parse_attribute(data_ammo, "category")
        self.icon = _parse_attribute(data_ammo, "icon")
        self.quantity = int(_parse_attribute(data_ammo, "quantity") or 0)
