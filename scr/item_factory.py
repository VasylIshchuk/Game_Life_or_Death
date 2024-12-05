from game_entity import _load_data_from_file, _parse_attribute
from weapon import Weapon
from ammo import Ammo


class ItemFactory:
    @staticmethod
    def create_item(title):
        data_item = _load_data_from_file("../items.json", title)
        category = _parse_attribute(data_item, "category")
        if category == "Weapon":
            return Weapon(title)
        elif category == "Ammo":
            return Ammo(title)
        elif category is None:
            raise ValueError(f"Unknown category for title: {title}")
