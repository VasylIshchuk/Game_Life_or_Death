from .creature import Creature
from ..core.game_entity import initialize_additional_attributes_from_data
from ..items.gear.equipment import Equipment
from ..items.gear.backpack import Backpack
from ..items.item_factory import ItemFactory


class Hero(Creature):
    def __init__(self, title):
        super().__init__(title)

        self.mental_state = None
        self.attack_range_spirit_power = None
        self.spiritual_power = None
        self.experience_points: int = 0

        attributes = ["mental_state", "attack_range_spirit_power", "spiritual_power"]
        initialize_additional_attributes_from_data(self, attributes, self.data_creature)

        self.equipment = Equipment()
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
        weapon_title = inventory.get("weapon")
        weapon = ItemFactory.create_item(weapon_title)

        self.equipment.equip_new_item(weapon)

    def _add_food_items_to_backpack(self, inventory):
        food_items = inventory.get("food", {})
        for food_title, count in food_items.items():
            for _ in range(count):
                self._add_food_item(food_title)

    def _add_food_item(self, food_title):
        food = ItemFactory.create_item(food_title)
        self.add_item_to_backpack(food)

    def get_defense(self):
        return self._apply_armor_effect() + self.equipment.get_artifact_effect("DefensiveRelic")

    def _apply_armor_effect(self):
        if self.equipment.has_armor():
            return self.equipment.get_armor_effect()
        return 0

    def get_agility(self):
        if self.equipment.has_artifact("SurvivalRelic"):
            self.equipment.decrease_artefact_durability(1)
        return self.agility + self.equipment.get_artifact_effect("SurvivalRelic")

    def get_attack_power(self):
        return (self.attack_power + self.equipment.get_weapon_effect() +
                self.equipment.get_artifact_effect("PowerRelic") +
                self._get_cursed_artifact_effect("CursedPowerRelic"))

    def get_spiritual_power(self):
        return (self.spiritual_power + self.equipment.get_artifact_effect("SpiritualRelic") +
                self._get_cursed_artifact_effect("CursedSpiritualRelic"))

    def get_attack_range(self):
        return self.equipment.get_weapon_strike_distance() if self.equipment.is_weapon_usable() else self.attack_range

    def _get_cursed_artifact_effect(self, cursed_relic_type):
        effect = self.equipment.get_artifact_effect(cursed_relic_type)
        if effect:
            self._apply_cursed_relic_penalty()
        return effect

    def _apply_cursed_relic_penalty(self):
        health_cost = self.equipment.get_cursed_relic_health_cost()
        self.decrease_health_points(health_cost)

    def set_spiritual_power(self, value):
        self.spiritual_power = value

    def update_defense(self, value):
        self.equipment.update_armor_defence(value)
        self.equipment.remove_armor_if_needed()
        if self.equipment.has_artifact("DefensiveRelic"): self.equipment.decrease_artefact_durability(1)

    def apply_book_effect(self):
        if self.equipment.has_book():
            new_spiritual_power = self.spiritual_power + self.equipment.get_book_effect()
            self.set_spiritual_power(new_spiritual_power)
            self.equipment.delete_book()

    def apply_food_effect(self):
        if self.equipment.has_food():
            effect = self.equipment.get_food_effect()
            self.healing(effect)
            self.equipment.delete_food()

    def get_key_from_slots(self):
        return self.equipment.get_key()

    def delete_key_from_slots(self):
        self.equipment.delete_key()

    def add_item_to_backpack(self, item):
        return self.backpack.add_item(item)

    def get_item_from_backpack(self, slot_index):
        return self.backpack.get_item(slot_index)

    def delete_item_from_backpack(self, slot_index):
        return self.backpack.remove_item_from_backpack(slot_index)

    def add_item_to_slots(self, item):
        return self.equipment.equip_new_item(item)

    def get_item_from_slots(self, item):
        return self.equipment.retrieve_equipped_item(item)

    def delete_item_from_slots(self, item):
        return self.equipment.remove_equipped_item(item)

    def validate_is_slot_available(self, item):
        return self.equipment.is_slot_available(item)

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
        self.decrease_health_points(total_damage)

    def _calculate_total_poison_damage(self):
        return len(self.poison_effect_rounds)

    def _update_poison_effects(self):
        self.poison_effect_rounds = [r - 1 for r in self.poison_effect_rounds if r > 1]

    def attack(self, enemy, game_map=None):
        if self._is_attack_ineffective(enemy): return

        self._execute_attack(enemy, self.get_attack_power())

        if (self.equipment.has_artifact("CursedPowerRelic") or
                self.equipment.has_artifact("PowerRelic")):
            self.equipment.decrease_artefact_durability(1)

    def _is_attack_ineffective(self, enemy):
        return (
                enemy.type == "phantom" or
                (enemy.title == "Winged Nightmare" and (
                        not self.equipment.has_weapon() or self.equipment.get_weapon_strike_distance() < 2))
        )

    def spiritual_attack(self, enemy):
        self._execute_attack(enemy, self.get_spiritual_power())
        if (self.equipment.has_artifact("CursedSpiritualRelic") or
                self.equipment.has_artifact("SpiritualRelic")):
            self.equipment.decrease_artefact_durability(1)

    def _execute_attack(self, enemy, attack_power):
        self._apply_special_conditions_pre_attack(enemy)
        self.luck = self._roll_dice()

        hit_probability = self._calculate_hit_probability(attack_power, enemy)

        if self._is_hit_successful(hit_probability):
            self._apply_damage_to_enemy(enemy, attack_power)
            self._decrease_weapon_durability()
            self._apply_special_conditions_post_attack(enemy)

        self._handle_experience(enemy)

    def _apply_special_conditions_pre_attack(self, enemy):
        if enemy.title == "Fire Choker": enemy.apply_abilities(self)

    def _decrease_weapon_durability(self):
        if self.equipment.is_weapon_usable():
            self.equipment.decrease_weapon_durability(1)
            if self.equipment.weapon_is_broken():
                self.equipment.delete_weapon()

    def _apply_special_conditions_post_attack(self, enemy):
        if enemy.title == "Angry Guardian": enemy.apply_abilities()
        if enemy.title == "Poisoned Monk": enemy.apply_abilities(self)

    def _handle_experience(self, enemy):
        if not enemy.is_alive and not self._is_at_max_level():
            experience_points = self._calculate_xp_for_enemy(enemy)
            self.add_experience_points(experience_points)

    def _is_at_max_level(self):
        MAX_LEVEL = 5
        return self.level >= MAX_LEVEL

    def _calculate_xp_for_enemy(self, enemy):
        return (enemy.level + 1) ** 2

    def calculate_xp_for_map_level_up(self, map_level):
        return (map_level + 1) * 10

    def add_experience_points(self, points):
        total_xp = self.experience_points + points
        xp_for_level_up = self.get_xp_required_for_level_up()

        if total_xp >= xp_for_level_up:
            self.experience_points = total_xp - xp_for_level_up
            self._level_up()
        else:
            self.experience_points = total_xp

    def get_xp_required_for_level_up(self):
        return (self.level + 1) ** 2 * 10

    def _level_up(self):
        self._increase_level()
        self._increase_attack_power()
        self._increase_spiritual_power()
        self._increase_agility()

    def _increase_attack_power(self):
        self.attack_power += self.level + 2

    def _increase_spiritual_power(self):
        self.spiritual_power += self.level

    def _increase_agility(self):
        self.agility += self.level + 3

    def _increase_level(self):
        self.level += 1
