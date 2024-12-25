from ..core.game_entity import GameEntity, load_data_from_file, initialize_general_attributes


class Ammo(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.category: str = ""
        self.icon: str = ""
        self.quantity: int = 0

        data_ammo = load_data_from_file("./items.json", title)
        initialize_general_attributes(self, data_ammo)
