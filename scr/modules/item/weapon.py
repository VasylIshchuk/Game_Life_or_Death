from .ammo import Ammo
from ..core.game_entity import GameEntity, load_data_from_file, get_attribute, initialize_general_attributes


class Weapon(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.type: str = ""
        self.category: str = ""
        self.icon: str = ""
        self.durability: int = 0
        self.strike_power: int = 0
        self.strike_distance: int = 0

        data_weapon = load_data_from_file("./items.json", title)
        initialize_general_attributes(self, data_weapon)

        if self.type == "RangedWeapon":
            ammo = get_attribute(data_weapon, "ammo")
            self.ammo = Ammo(ammo)

        self.is_break = False
        self.shards = "*"
