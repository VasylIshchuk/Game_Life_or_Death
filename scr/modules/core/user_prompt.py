from .icons import Icon
from ..items.gear.equipment import EQUIPMENT_SLOTS


class UserPrompt:
    def __init__(self, hero, level_number):
        self.text = []
        self.hero = hero
        self.level_number = level_number
        self._initialize_stable_text()

    def get_text(self):
        return self.text

    def add_text(self, text):
        self.text.append(text)

    def reset_text(self):
        self.text.clear()
        self._initialize_stable_text()

    def _initialize_stable_text(self):
        self.add_text(f'Level: {self.level_number}')
        self.show_hero_stats()
        self.show_equipment()

    def show_hero_stats(self):
        stats = {
            "Health Points": self.hero.health_points,
            "Mental State": self.hero.mental_state,
            "Level": self.hero.level,
            "Defense": self.hero.get_defense(),
            "Attack Power": self.hero.get_attack_power(),
            "Spiritual Power": self.hero.get_spiritual_power(),
            "Agility": self.hero.agility,
            "Attack Range": self.hero.attack_range,
            "Attack Range (Spirit Power)": self.hero.attack_range_spirit_power,
            "Experience Points": self.hero.experience_points
        }

        self.text.append("Hero Stats:")
        for stat, value in stats.items():
            self.text.append(f"\t• {stat}: {value}")

    def show_backpack(self):
        self.append_new_line()
        self.text.append('Choose an item by entering a number, or press "q" to exit.')
        self.append_new_line()
        self.text.append('Backpack:')
        self._get_inventory_text(self.hero.backpack.get_slots())

    def append_new_line(self):
        self.text.append("")

    def show_chest_items(self, chest):
        self.append_new_line()
        self.text.append('Choose an item by entering a number, or press "q" to exit.')
        self.append_new_line()
        self.text.append('Chest items:')
        self._get_inventory_text(chest.get_slots())

    def _get_inventory_text(self, items):
        for index, item in enumerate(items, start=1):
            if item is None:
                self.text.append(f"\t· {index}) {Icon.EMPTY_SLOT}")
            else:
                self.text.append(f"\t· {index}) {item.icon} - {item.title} ({item.category})")
                self.show_attributes(item)

    def show_equipment(self):
        self.append_new_line()
        self.text.append("Equipment:")
        for slot_title, index in EQUIPMENT_SLOTS.items():
            item = self.hero.equipment.get_item(index)
            self.text.append(self._get_equipment_item_text(index + 1, slot_title, item))

    def _get_equipment_item_text(self, index, slot_title, item):
        if item is None:
            return f"\t· {index}) {slot_title} - {Icon.EMPTY_SLOT}"
        else:
            return f"\t· {index}) {slot_title} - {item.icon} \"{item.title}\""

    def show_item_action_menu(self):
        self.append_new_line()
        options = {
            "U": "Equip or use an item",
            "D": "Drop an item in chest",
            "E": "Exchange an item with an item in the chest",
            "S": "View character stats",
            "Q": "Return back"
        }
        self._display_options("Select an action:", options)

    def show_floor_direction_menu(self):
        self.append_new_line()
        options = {
            "1": "Move up",
            "2": "Move down"
        }
        self._display_options("Select a direction:", options)

    def _display_options(self, title, options):
        self.text.append(f"{title}")
        for key, desc in options.items():
            self.text.append(f"· {key} – {desc}")

    def show_backpack_is_full(self):
        self.append_new_line()
        self.text.append("BACKPACK IS FULL")

    def show_chest_is_empty(self):
        self.append_new_line()
        self.text.append('Chest is empty ;(')

    def show_item_stats(self, item):
        self.text.append("")
        self.text.append(f"{item.icon} - {item.title}")
        self.show_attributes(item)

    def show_attributes(self, item):
        for attr_name, value in item.__dict__.items():
            if attr_name in ("icon", "title", "position"): continue
            self.text.append(f"\t\t{attr_name}: {value}")
