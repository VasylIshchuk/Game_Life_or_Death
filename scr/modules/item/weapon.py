from .ammo import Ammo
from ..core.game_entity import GameEntity, load_data_from_file, parse_attribute, initialize_general_attributes


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

        # self.type = parse_attribute(data_weapon, "type")
        if self.type == "RangedWeapon":
            ammo = parse_attribute(data_weapon, "ammo")
            self.ammo = Ammo(ammo)

        self.is_break = False
        self.shards = "*"

        # self.category = parse_attribute(data_weapon, "category")
        # self.icon = parse_attribute(data_weapon, "icon")
        # self.durability = int(parse_attribute(data_weapon, "durability") or 0)
        # self.strike_power = int(parse_attribute(data_weapon, "strike_power") or 0)
        # self.strike_distance = int(parse_attribute(data_weapon, "strike_distance") or 0)
