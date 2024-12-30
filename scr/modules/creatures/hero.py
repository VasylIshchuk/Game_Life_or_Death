from .creature import Creature
from ..core.game_entity import initialize_additional_attributes_from_data, get_attribute_from_data
from ..items.inventory import Inventory
from ..items.weapon import Weapon


class Hero(Creature):
    def __init__(self, title):
        super().__init__(title)

        self.mental_state = None
        self.attack_range_spirit_power = None
        self.spiritual_power = None

        attributes = ["mental_state", "attack_range_spirit_power", "spiritual_power"]
        initialize_additional_attributes_from_data(self, attributes, self.data_creature)
        self._initialize_inventory(get_attribute_from_data(self.data_creature, "inventory"))

        self.poison_effect_rounds = []
        self.is_poisoned = False
        self.is_crazy = False

    def _initialize_inventory(self, inventory_data: dict):
        self.weapon = Weapon(get_attribute_from_data(inventory_data, "weapon"))
        self.inventory = Inventory()

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

        attack_power = self.attack_power + self._apply_weapon_damage()
        self._execute_attack(enemy, attack_power)

    def _is_attack_ineffective(self, enemy):
        return (
                enemy.type == "phantom" or
                (enemy.title == "Winged Nightmare" and (not self.weapon or self.weapon.strike_distance < 2))
        )

    def _apply_weapon_damage(self):
        if self.weapon and not self.weapon.is_break:
            return self.weapon.strike_power
        return 0

    def spiritual_attack(self, enemy):
        self._execute_attack(enemy, self.spiritual_power)

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
        if self.weapon:
            self.weapon.durability -= 1
            if self.weapon.durability <= 0:
                self.weapon.is_break = True

    def _apply_special_conditions_post_attack(self, enemy):
        if enemy.title == "Angry Guardian": enemy.apply_abilities()
        if enemy.title == "Poisoned Monk": enemy.apply_abilities(self)
