from .forest import Forest
from .forest_item_spawner import ForestItemSwamper
from ...items.item_factory import ItemFactory

WIDTH = 35
HEIGHT = 30


class MountainPeak(Forest):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT)
        item = ItemFactory.create_item("Flower")
        ForestItemSwamper(self).place_item_in_forest(item)

