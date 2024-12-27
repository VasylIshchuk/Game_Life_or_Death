from ..core.game_entity import GameEntity, load_data_from_file, initialize_attributes_from_data


class Ammo(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.category: str = ""
        self.icon: str = ""
        self.quantity: int = 0

        data_ammo = load_data_from_file("./items.json", title)
        initialize_attributes_from_data(self, data_ammo)
