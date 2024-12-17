from .creature import Creature
from ..item.inventory import Inventory
import random


class Hero(Creature):
    def __init__(self, title):
        super().__init__(title)

        self.mental_state = None
        self.attack_range_spirit_power = None
        self.spiritual_power = None

        self.poison_effect_rounds = []
        self.is_poisoned = False
        self.is_crazy = False

        attributes = ["mental_state", "attack_range_spirit_power", "spiritual_power"]
        self._initialize_general_attributes(attributes)
        self.inventory = Inventory()

    def check_mental_state(self):
        if self.mental_state <= 0:
            self.is_crazy = True

    def apply_poison(self, rounds):
        """Applies a poison effect for a certain number of rounds."""
        self.poison_effect_rounds.append(rounds)
        self.is_poisoned = True

    def update_status(self):
        """Updates the hero's state on each game turn."""
        if self.is_poisoned:
            self._process_poison_effect()
            if not self.poison_effect_rounds:
                self.is_poisoned = False

    def physical_attack(self, enemy):
        """Executes a physical attack against the target."""
        if self._is_attack_ineffective(enemy): return

        attack_power = self.attack_power + self._apply_weapon_damage()
        self._execute_attack(enemy, attack_power)

    def spiritual_attack(self, enemy):
        """Executes a spiritual attack against the target."""
        self._execute_attack(enemy, self.spiritual_power)

    def _execute_attack(self, enemy, attack_power):
        """Calculates and applies the result of an attack."""
        self._apply_special_conditions_pre_attack(enemy)
        result_dice = random.randint(1, 20)

        hit_chance = self.calculate_hit_chance(enemy, attack_power, result_dice)
        random_factor = random.random()

        if result_dice == 20 or (result_dice != 1 and random_factor <= hit_chance):
            self._apply_damage_to_enemy(enemy, attack_power)
            self._decrease_weapon_durability()
            self._apply_special_conditions_post_attack(enemy)

        self._process_poison_effect()

    def _is_attack_ineffective(self, enemy):
        """Determines if the physical attack is ineffective due to specific conditions."""
        return (
                enemy.type == "phantom" or
                (enemy.title == "Winged Nightmare" and (not self.weapon or self.weapon.strike_distance < 2))
        )

    def _apply_special_conditions_pre_attack(self, enemy):
        """Applies pre-attack special conditions based on the enemy."""
        if enemy.title == "Fire Choker": enemy.apply_skills(self)

    def _apply_special_conditions_post_attack(self, enemy):
        """Applies post-attack special conditions based on the enemy."""
        if enemy.title == "Angry Guardian": enemy.apply_skills()
        if enemy.title == "Poisoned Monk": enemy.apply_skills(self)

    def _process_poison_effect(self):
        """Applies damage from all active poison effects."""
        if self.poison_effect_rounds:
            # We list the current damage
            total_damage = len(self.poison_effect_rounds)

            self.health_points -= total_damage
            self.check_is_alive()

            # Update rounds counters
            self.poison_effect_rounds = [r - 1 for r in self.poison_effect_rounds if r > 1]

    def _decrease_weapon_durability(self):
        """Decreases the weapon's durability and marks it as broken if necessary."""
        if self.weapon:
            self.weapon.durability -= 1
            if self.weapon.durability <= 0:
                self.weapon.is_break = True

    def _apply_weapon_damage(self):
        """Applies the weapon's bonus to the attack if it is not broken and used."""
        if self.weapon and not self.weapon.is_break:
            return self.weapon.strike_power
        return 0
