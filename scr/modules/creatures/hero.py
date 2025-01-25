from .creature import Creature
from ..core.game_entity import initialize_additional_attributes_from_data
from ..items.food import Food
from ..items.inventory.slots import Slots
from ..items.inventory.backpack import Backpack


class Hero(Creature):
    def __init__(self, title):
        super().__init__(title)

        self.mental_state = None
        self.attack_range_spirit_power = None
        self.spiritual_power = None

        attributes = ["mental_state", "attack_range_spirit_power", "spiritual_power"]
        initialize_additional_attributes_from_data(self, attributes, self.data_creature)

        self.slots = Slots()
        self.backpack = Backpack()
        self._initialize_inventory()

        self.poison_effect_rounds = []
        self.is_poisoned = False
        self.is_crazy = False

    def _initialize_inventory(self):
        inventory = self.data_creature.get("inventory", {})
        self._add_weapon_to_slots(inventory)
        self._add_food_items_to_backpack(inventory)

    def _add_weapon_to_slots(self, inventory):
        weapon = inventory.get("weapon")
        self.slots.add_item(weapon)

    def _add_food_items_to_backpack(self, inventory):
        food_items = inventory.get("food", {})
        for food_name, count in food_items.items():
            for _ in range(count):
                self._add_food_item(food_name)

    def _add_food_item(self, food_name):
        food = Food(food_name)
        self.add_item_to_backpack(food)

    def get_defense(self):
        return self.defense + self.slots.get_artifact_effect("DefensiveRelic")

    def get_agility(self):
        return self.agility + self.slots.get_artifact_effect("SurvivalRelic")

    def get_attack_power(self):
        return (self.attack_power + self.slots.get_weapon_effect() + self.slots.get_artifact_effect("PowerRelic") +
                self._get_cursed_artifact_effect("CursedPowerRelic"))

    def get_spiritual_power(self):
        return (self.spiritual_power + self.slots.get_artifact_effect("SpiritualRelic") +
                self._get_cursed_artifact_effect("CursedSpiritualRelic"))

    def _get_cursed_artifact_effect(self, cursed_relic_type):
        effect = self.slots.get_artifact_effect(cursed_relic_type)
        if effect:
            self._apply_cursed_relic_penalty()
        return effect

    def _apply_cursed_relic_penalty(self):
        health_cost = self.slots.get_cursed_relic_health_cost()
        self.health_points -= health_cost

    def set_spiritual_power(self, value):
        self.spiritual_power = value

    def set_defense(self, value):
        self.defense = value
        self._remove_armor_if_needed()

    def _remove_armor_if_needed(self):
        if self.defense == 0 and self.slots.has_armor():
            self.slots.delete_armor()

    def apply_book_effect(self):
        new_spiritual_power = self.spiritual_power + self.slots.get_book_effect()
        self.set_spiritual_power(new_spiritual_power)
        self.slots.delete_book()

    def apply_armor_effect(self):
        effect = self.slots.get_armor_effect()
        self.set_defense(effect)

    def apply_food_effect(self):
        effect = self.slots.get_food_effect
        self.healing(effect)
        self.slots.delete_food()

    def add_item_to_backpack(self, item):
        return self.backpack.add_item(item)

    def get_item_from_backpack(self, slot_index):
        return self.backpack.get_item(slot_index)

    def delete_item_from_backpack(self, slot_index):
        return self.backpack.delete_item(slot_index)

    def add_item_to_slots(self, item):
        return self.slots.add_item(item)

    def get_item_from_slots(self, slot_index):
        return self.slots.get_item(slot_index)

    def delete_item_from_slots(self, slot_index):
        return self.slots.delete_item(slot_index)

    def check_mental_state(self):
        if self.mental_state <= 0:
            self.is_crazy = True

    def decrease_mental_state(self, points):
        self.mental_state -= points
        self.check_mental_state()

    def apply_poison_effect(self, rounds):
        self.poison_effect_rounds.append(rounds)
        self.is_poisoned = True

    def update_status(self):
        """TODO: Updates the hero's state on each game turn."""
        if self.is_poisoned:
            self._process_poison_effect()
            if not self.poison_effect_rounds:
                self.is_poisoned = False

    def _process_poison_effect(self):
        if self.poison_effect_rounds:
            self._apply_poison_damage()
            self._update_poison_effects()

    def _apply_poison_damage(self):
        total_damage = self._calculate_total_poison_damage()
        self.health_points -= total_damage
        self.check_is_alive()

    def _calculate_total_poison_damage(self):
        return len(self.poison_effect_rounds)

    def _update_poison_effects(self):
        self.poison_effect_rounds = [r - 1 for r in self.poison_effect_rounds if r > 1]

    def attack(self, enemy):
        if self._is_attack_ineffective(enemy): return

        self._execute_attack(enemy, self.get_attack_power())

    def _is_attack_ineffective(self, enemy):
        return (
                enemy.type == "phantom" or
                (enemy.title == "Winged Nightmare" and (
                        not self.slots.has_weapon() or self.slots.get_weapon_strike_distance() < 2))
        )

    def spiritual_attack(self, enemy):
        self._execute_attack(enemy, self.get_spiritual_power())

    def _execute_attack(self, enemy, attack_power):
        self._apply_special_conditions_pre_attack(enemy)
        self.luck = self._roll_dice()

        hit_probability = self._calculate_hit_probability(attack_power, enemy)

        if self._is_hit_successful(hit_probability):
            self._apply_damage_to_enemy(enemy, attack_power)
            self._decrease_weapon_durability()
            self._apply_special_conditions_post_attack(enemy)

    def _apply_special_conditions_pre_attack(self, enemy):
        if enemy.title == "Fire Choker": enemy.apply_abilities(self)

    def _decrease_weapon_durability(self):
        if self.slots.has_weapon():
            self.slots.decrease_weapon_durability(1)
            if self.slots.weapon_is_broken():
                self.slots.delete_weapon()

    def _apply_special_conditions_post_attack(self, enemy):
        if enemy.title == "Angry Guardian": enemy.apply_abilities()
        if enemy.title == "Poisoned Monk": enemy.apply_abilities(self)
