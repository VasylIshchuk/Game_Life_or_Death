from ..inventory import Inventory

_SLOTS = {
    "Food": 0,
    "Book": 1,
    "Artifact": 2,
    "Weapon": 3,
    "Ammo": 4,
    "Armor": 5,
    "Key": 6
}


def _get_slot_index(category):
    return _SLOTS[category]


class Equipment(Inventory):
    food_slot_index = _get_slot_index("Food")
    book_slot_index = _get_slot_index("Book")
    artifact_slot_index = _get_slot_index("Artifact")
    weapon_slot_index = _get_slot_index("Weapon")
    ammo_slot_index = _get_slot_index("Ammo")
    armor_slot_index = _get_slot_index("Armor")
    key_slot_index = _get_slot_index("Key")

    def __init__(self, size=len(_SLOTS)):
        super().__init__(size)

    def add_item(self, item):
        slot_category = item.category
        slot_index = _get_slot_index(slot_category)
        if not self._is_slot_available(slot_index): return False
        self.slots[slot_index] = item
        return True

    def _is_slot_available(self, index):
        return index < self.size and self.slots[index] is None

    def has_weapon(self):
        return self._slot_has_item(self.weapon_slot_index)

    def delete_weapon(self):
        self.delete_item(self.weapon_slot_index)

    def weapon_is_broken(self):
        weapon = self.get_item(self.weapon_slot_index)
        return weapon.is_broken

    def decrease_weapon_durability(self, value):
        weapon = self.get_item(self.weapon_slot_index)
        weapon.decrease_durability(value)

    def get_weapon_strike_distance(self):
        weapon = self.get_item(self.weapon_slot_index)
        return weapon.strike_distance

    def get_weapon_effect(self):
        if not self._is_weapon_usable():
            return 0

        self._handle_ranged_weapon()

        weapon_power = self._get_weapon_strike_power()
        if self._has_artifact("WarriorsRelic"):
            return weapon_power + self.get_artifact_effect("WarriorsRelic")

        return weapon_power

    def _is_weapon_usable(self):
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
        return self._slot_has_item(self.ammo_slot_index)

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
        artifact = self.get_item(self.artifact_slot_index)
        return self._slot_has_item(self.artifact_slot_index) and artifact.type == artifact_type

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

    def get_book_effect(self):
        book = self.get_item(self.book_slot_index)
        return book.effect

    def delete_book(self):
        self.delete_item(self.book_slot_index)

    def get_food_effect(self):
        food = self.get_item(self.food_slot_index)
        return food.effect

    def delete_food(self):
        self.delete_item(self.food_slot_index)

    def has_armor(self):
        return self._slot_has_item(self.armor_slot_index)

    def get_armor_effect(self):
        armor = self.get_item(self.armor_slot_index)
        return armor.effect

    def delete_armor(self):
        self.delete_item(self.armor_slot_index)
