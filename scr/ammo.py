from item import Item


class Ammo(Item):
    def __init__(self, title):
        super().__init__(title)

        data_ammo = self.load_data_from_file("../items.json", title)
        self.category = self.parse_attribute(data_ammo, "category")
        self.icon = self.parse_attribute(data_ammo, "icon")
        self.quantity = int(self.parse_attribute(data_ammo, "quantity") or 0)
