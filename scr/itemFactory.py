from game_entity import GameEntity
from weapon import Weapon
from ammo import Ammo


class ItemFactory:
    @staticmethod
    def create_item(title):
        data_item = GameEntity.load_data_from_file("../items.json", title)
        category = GameEntity.parse_attribute(data_item, "category")
        if category == "Weapon":
            return Weapon(title)
        elif category == "Ammo":
            return Ammo(title)
        elif category is None:
            raise ValueError(f"Unknown category for title: {title}")
