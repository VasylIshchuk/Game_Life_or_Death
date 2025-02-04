from ..core.game_entity import get_attribute_from_data
from ..core.data_loader import load_entity_data_from_file
from .weapon import Weapon
from .ammo import Ammo
from .armor import Armor
from .food import Food
from .book import Book
from .misc import OtherItem
from .artifact import Artifact
from .artifacts.cursed_relic import CursedRelic
from .chests.closed_chest import ClosedChest
from .chests.ordinary_chest import OrdinaryChest
from .key import Key

_CATEGORY_ITEMS = {
    "Weapon": Weapon,
    "Ammo": Ammo,
    "Armor": Armor,
    "Food": Food,
    "Book": Book,
    "Misc": OtherItem,
    "OrdinaryChest": OrdinaryChest,
    "ClosedChest": ClosedChest,
    "Key": Key
}

_TYPE_INVENTORY = {
    "SpiritualRelic": Artifact,
    "CursedSpiritualRelic": CursedRelic,
    "DefensiveRelic": Artifact,
    "SurvivalRelic": Artifact,
    "PowerRelic": Artifact,
    "WarriorsRelic": Artifact,
    "CursedPowerRelic": CursedRelic
}


def get_class(data_item, category):
    if category == "Artifact":
        type = get_attribute_from_data(data_item, "type")
        return _TYPE_INVENTORY.get(type)
    else:
        return _CATEGORY_ITEMS.get(category)


class ItemFactory:
    @staticmethod
    def create_item(title):
        data_item = load_entity_data_from_file("./items.json", title)
        category = get_attribute_from_data(data_item, "category")
        item_class = get_class(data_item, category)
        return item_class(title)
