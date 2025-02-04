import json


def load_entity_data_from_file(file_path: str, title: str) -> dict:
    data = load_data_from_file(file_path)
    if title not in data:
        raise ValueError(f"{title} not found in the JSON file.")
    return data[title]


def load_data_from_file(file_path: str):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("File not found")
        raise
    except json.JSONDecodeError:
        print("Invalid JSON format")
        raise
