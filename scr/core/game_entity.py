import os
import json

from ..map.position import Position


def _parse_attribute(data_creature: dict, attribute_name: str):
    return data_creature.get(attribute_name)


def _load_data_from_file(file_path: str, title: str) -> dict:
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(base_dir, "..", file_name)
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


class GameEntity:
    def __init__(self, title):
        self.title = title
        self.position = None

    def set_position(self, position: Position):
        self.position = position
