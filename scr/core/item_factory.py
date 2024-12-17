from ..core.game_entity import  _load_data_from_file, _parse_attribute
from ..item.weapon import Weapon
from ..item.ammo import Ammo


class ItemFactory:
    @staticmethod
    def create_item(title):
        data_items = _load_data_from_file("./items.json", title)
        category = _parse_attribute(data_items, "category")
        if category == "Weapon":
            return Weapon(title)
        elif category == "Ammo":
            return Ammo(title)
        elif category is None:
            raise ValueError(f"Unknown category for title: {title}")
