from .ammo import Ammo
from ..core.game_entity import GameEntity, _load_data_from_file, _parse_attribute


class Weapon(GameEntity):
    def __init__(self, title):
        super().__init__(title)

        data_weapon = _load_data_from_file("./items.json", title)

        self.type = _parse_attribute(data_weapon, "type")
        if self.type == "ranged":
            ammo = _parse_attribute(data_weapon, "ammo")
            self.ammo = Ammo(ammo)

        self.is_break = False
        self.category = _parse_attribute(data_weapon, "category")
        self.icon = _parse_attribute(data_weapon, "icon")
        self.durability = int(_parse_attribute(data_weapon, "durability") or 0)
        self.strike_power = int(_parse_attribute(data_weapon, "strike_power") or 0)
        self.strike_distance = int(_parse_attribute(data_weapon, "strike_distance") or 0)
        self.shards = "*"
