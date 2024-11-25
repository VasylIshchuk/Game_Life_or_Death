from item import Item
from ammo import Ammo


class Weapon(Item):
    def __init__(self, title):
        super().__init__(title)

        data_weapon = self.load_data_from_file("../items.json", title)

        self.type = self.parse_attribute(data_weapon, "type")
        if self.type == "ranged":
            ammo = self.parse_attribute(data_weapon, "ammo")
            self.ammo = Ammo(ammo)

        self.is_break = False
        self.category = self.parse_attribute(data_weapon, "category")
        self.icon = self.parse_attribute(data_weapon, "icon")
        self.durability = int(self.parse_attribute(data_weapon, "durability") or 0)
        self.strike_power = int(self.parse_attribute(data_weapon, "strike_power") or 0)
        self.strike_distance = int(self.parse_attribute(data_weapon, "strike_distance") or 0)
        self.shards = "*"
