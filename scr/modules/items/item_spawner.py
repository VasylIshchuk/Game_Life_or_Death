import random
from .item_factory import ItemFactory
from ..core.game_entity import load_data_from_file

ITEMS_FILE_PATH = "./items.json"
PROBABILITY_ADD_CLOSED_CHEST = 0.15
EXCLUDED_ITEMS = {"Key", "Corpse","Statue with a Cup", "Ordinary Chest", "Closed Chest"}


class ItemSpawner:
    def __init__(self, map):
        self._map = map

    def generate_chest(self):
        chest_item = self._get_chest()
        chest = ItemFactory().create_item(chest_item)
        self._initialize_chest(chest)
        return chest

    def _get_chest(self):
        if random.random() < PROBABILITY_ADD_CLOSED_CHEST:
            return "Closed Chest"
        return "Ordinary Chest"

    def _initialize_chest(self, chest):
        for i in range(len(chest.slots)):
            data_items = load_data_from_file(ITEMS_FILE_PATH)
            filtered_items = [name for name, data in data_items.items() if name not in EXCLUDED_ITEMS]
            item_title = random.choice(filtered_items)
            item = ItemFactory().create_item(item_title)
            chest.slots[i] = item
