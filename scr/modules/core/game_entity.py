import json

from ..map.position import Position


def get_attribute(entity_data: dict, attribute_name: str):
    """Fetches the value of the given attribute from the data dictionary."""
    return entity_data.get(attribute_name)


def load_data_from_file(file_path: str, title: str) -> dict:
    """Loads data from a JSON file and retrieves the entry corresponding to the 'title'."""
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


def initialize_additional_attributes(self, attributes: list[str], entity_data: dict):
    """Initializes additional attributes for the entity based on the given list."""
    for attr in attributes:
        setattr(self, attr, get_attribute(entity_data, attr))


def initialize_general_attributes(self, entity_data: dict):
    """Initializes general attributes for the entity from the provided data."""
    for key, value in entity_data.items():
        if hasattr(self, key):
            setattr(self, key, value)


class GameEntity:
    def __init__(self, title):
        self.title = title
        self.position = None

    def set_position(self, position: Position):
        self.position = position
