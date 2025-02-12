from ..inventory import Inventory

EQUIPMENT_SLOTS = {
    "Food": 0,
    "Book": 1,
    "Artifact": 2,
    "Weapon": 3,
    "Ammo": 4,
    "Armor": 5,
    "Key": 6
}


def _get_slot_index(category):
    return EQUIPMENT_SLOTS[category]


class Equipment(Inventory):
    food_slot_index = _get_slot_index("Food")
    book_slot_index = _get_slot_index("Book")
    artifact_slot_index = _get_slot_index("Artifact")
    weapon_slot_index = _get_slot_index("Weapon")
    ammo_slot_index = _get_slot_index("Ammo")
    armor_slot_index = _get_slot_index("Armor")
    key_slot_index = _get_slot_index("Key")

    def __init__(self, size=len(EQUIPMENT_SLOTS)):
        super().__init__(size)

    def equip_new_item(self, item):
        slot_index = self._get_slot_index_from(item)
        if self.slot_has_item(slot_index): return False
        self.slots[slot_index] = item
        return True

    def retrieve_equipped_item(self, item):
        slot_index = self._get_slot_index_from(item)
        if not self.slot_has_item(slot_index): return None
        return self.get_item(slot_index)

    def remove_equipped_item(self, item):
        slot_index = self._get_slot_index_from(item)
        if not self.slot_has_item: return False
        self.slots[slot_index] = None
        return True

    def _get_slot_index_from(self, item):
        slot_category = item.category
        return _get_slot_index(slot_category)

    def is_slot_available(self, item):
        slot_index = self._get_slot_index_from(item)
        if self.slot_has_item(slot_index): return False
        return True

    def has_weapon(self):
        return self.slot_has_item(self.weapon_slot_index)

    def delete_weapon(self):
        self.delete_item(self.weapon_slot_index)

    def weapon_is_broken(self):
        weapon = self.get_item(self.weapon_slot_index)
        return weapon.is_broken()

    def decrease_weapon_durability(self, value):
        weapon = self.get_item(self.weapon_slot_index)
        weapon.decrease_durability(value)

    def get_weapon_strike_distance(self):
        weapon = self.get_item(self.weapon_slot_index)
        return weapon.strike_distance

    def get_weapon_effect(self):
        if not self.is_weapon_usable():
            return 0

        self._handle_ranged_weapon()

        weapon_power = self._get_weapon_strike_power()
        if self._has_artifact("WarriorsRelic"):
            return weapon_power + self.get_artifact_effect("WarriorsRelic")

        return weapon_power

    def is_weapon_usable(self):
        if not self.has_weapon():
            return False

        if self._is_ranged_weapon() and not self._validate_ranged_weapon_ammo():
            return False

        return True

    def _is_ranged_weapon(self):
        return self._get_weapon_type() == "RangedWeapon"

    def _get_weapon_type(self):
        weapon = self.get_item(self.weapon_slot_index)
        return weapon.type

    def _validate_ranged_weapon_ammo(self):
        if not self._has_ammo():
            return False

        if not self._ammo_is_usable():
            self._delete_ammo()
            return False

        return True

    def _has_ammo(self):
        return self.slot_has_item(self.ammo_slot_index)

    def _ammo_is_usable(self):
        ammo = self.get_item(self.ammo_slot_index)
        return ammo.is_usable()

    def _delete_ammo(self):
        self.delete_item(self.ammo_slot_index)

    def _handle_ranged_weapon(self):
        if self._is_ranged_weapon():
            self._ammo_decrease_quantity()

    def _ammo_decrease_quantity(self):
        ammo = self.get_item(self.ammo_slot_index)
        return ammo.decrease_quantity()

    def _get_weapon_strike_power(self):
        weapon = self.get_item(self.weapon_slot_index)
        return weapon.strike_power

    def get_artifact_effect(self, artifact_type):
        if self._has_artifact(artifact_type):
            effect = self._process_artifact_effect()
            return effect
        return 0

    def _has_artifact(self, artifact_type):
        if self.slot_has_item(self.artifact_slot_index):
            artifact = self.get_item(self.artifact_slot_index)
            return artifact.type == artifact_type
        return False

    def _process_artifact_effect(self):
        if not self._artifact_is_usable():
            self._delete_artifact()
            return 0
        self._decrease_artefact_durability(1)
        return self._get_artifact_effect()

    def _artifact_is_usable(self):
        artifact = self.get_item(self.artifact_slot_index)
        return artifact.is_usable()

    def _delete_artifact(self):
        self.delete_item(self.artifact_slot_index)

    def _decrease_artefact_durability(self, value):
        artifact = self.get_item(self.artifact_slot_index)
        artifact.decrease_durability(value)

    def _get_artifact_effect(self):
        artifact = self.get_item(self.artifact_slot_index)
        return artifact.effect

    def get_cursed_relic_health_cost(self):
        artifact = self.get_item(self.artifact_slot_index)
        return artifact.health_cost

    def has_book(self):
        return self.slot_has_item(self.book_slot_index)

    def get_book_effect(self):
        book = self.get_item(self.book_slot_index)
        return book.effect

    def delete_book(self):
        self.delete_item(self.book_slot_index)

    def has_food(self):
        return self.slot_has_item(self.food_slot_index)

    def get_food_effect(self):
        food = self.get_item(self.food_slot_index)
        return food.effect

    def delete_food(self):
        self.delete_item(self.food_slot_index)

    def has_armor(self):
        return self.slot_has_item(self.armor_slot_index)

    def get_armor_effect(self):
        armor = self.get_item(self.armor_slot_index)
        return armor.get_defence_effect()

    def update_armor_defence(self, value):
        armor = self.get_item(self.armor_slot_index)
        armor.update_defence(value)

    def remove_armor_if_needed(self):
        if self.has_armor() and not self._armor_is_usable():
            self._delete_armor()

    def _armor_is_usable(self):
        armor = self.get_item(self.armor_slot_index)
        return armor.is_usable()

    def _delete_armor(self):
        self.delete_item(self.armor_slot_index)

    def get_key(self):
        return self.get_item(self.key_slot_index)

    def delete_key(self):
        self.delete_item(self.key_slot_index)
