import json

from ..maps.position import Position


def get_attribute_from_data(entity_data: dict, attribute_name: str):
    return entity_data.get(attribute_name)


def load_data_from_file(file_path: str, title: str) -> dict:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            if title not in data:
                raise ValueError(f"{title} not found in the JSON file.")
            return data[title]
    except FileNotFoundError:
        print("File not found")
        raise
    except json.JSONDecodeError:
        print("Invalid JSON format")
        raise


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
        self.position = None

    def set_position(self, position: Position):
        self.position = position
