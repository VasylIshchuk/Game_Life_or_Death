import random
from .item_factory import ItemFactory
from ..core.data_loader import load_data_from_file

ITEMS_FILE_PATH = "./items.json"
PROBABILITY_ADD_CLOSED_CHEST = 0.15
EXCLUDED_ITEMS = {"Ordinary Chest", "Closed Chest", "Key", "Human Corpse", "Statue with a Cup", "Flower"}


class ItemSpawner:
    def __init__(self, map):
        self._map = map

    def generate_chest(self):
        chest_title = self._select_chest()
        chest = ItemFactory().create_item(chest_title)
        return chest

    def _select_chest(self):
        if random.random() < PROBABILITY_ADD_CLOSED_CHEST:
            return "Closed Chest"
        return "Ordinary Chest"

    def initialize_chest(self, chest):
        for index in range(len(chest.get_slots())):
            data_items = load_data_from_file(ITEMS_FILE_PATH)
            filtered_items = [name for name, data in data_items.items() if name not in EXCLUDED_ITEMS]
            item_title = random.choice(filtered_items)
            item = ItemFactory().create_item(item_title)
            chest.set_item(index,item)
