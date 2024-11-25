import json

from position import Position


class GameEntity:
    def __init__(self, title):
        self.title = title
        self.position = None

    def set_position(self, position: Position):
        self.position = position

    @staticmethod
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

    @staticmethod
    def parse_attribute(data_creature: dict, attribute_name: str):
        return data_creature.get(attribute_name)