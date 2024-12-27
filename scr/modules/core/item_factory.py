from ..core.game_entity import load_data_from_file, get_attribute_from_data
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
        category = get_attribute_from_data(data_item, "category")
        item_class = _CATEGORY_ITEMS.get(category)
        return item_class(title)
