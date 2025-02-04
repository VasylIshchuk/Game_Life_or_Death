from ..maps.position import Position
from ..core.data_loader import load_entity_data_from_file


def get_attribute_from_data(entity_data: dict, attribute_name: str):
    return entity_data.get(attribute_name)


def initialize_additional_attributes_from_data(entity, attributes: list[str], entity_data: dict):
    for attr in attributes:
        setattr(entity, attr, get_attribute_from_data(entity_data, attr))


def initialize_attributes_from_data(entity, entity_data: dict):
    for key, value in entity_data.items():
        if hasattr(entity, key):
            setattr(entity, key, value)


class GameEntity:
    def __init__(self, title):
        self.title = title
        self.category: str = ""
        self.icon: str = ""
        self.position = None

    def set_position(self, position: Position):
        self.position = position

    def get_x_position(self):
        return self.position.get_x()

    def get_y_position(self):
        return self.position.get_y()

    def initialize_items_attributes(self):
        data_item = load_entity_data_from_file("./items.json", self.title)
        initialize_attributes_from_data(self, data_item)
