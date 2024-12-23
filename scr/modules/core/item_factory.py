from ..core.game_entity import load_data_from_file, parse_attribute
from ..item.weapon import Weapon
from ..item.ammo import Ammo

_CATEGORY_ITEMS = {
    "Weapon": Weapon,
    "Ammo": Ammo,
}


class ItemFactory:
    @staticmethod
    def create_item(title):
        data_item = load_data_from_file("./items.json", title)
        category = parse_attribute(data_item, "category")
        item = _CATEGORY_ITEMS.get(category)
        return item(title)
