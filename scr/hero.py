from creature import *
from inventory import Inventory


class Hero(Creature):
    def __init__(self, title):

        super().__init__(title)
        self.mental_state = None
        self.attack_range_spirit_power = None
        self.spiritual_power = None

        self.poison_damage_rounds = []
        self.is_poisoned = False

        attributes = ["mental_state", "attack_range_spirit_power", "spiritual_power"]
        self._initialize_general_attributes(attributes)
        self.inventory = Inventory()

    def add_poison_effect(self, rounds):
        """Adds a poison effect for a certain number of rounds."""
        self.damage_rounds.append(rounds)
        self.is_poisoned = True

    def update_status(self):
        """Updates the hero's state on each game turn."""
        if self.is_poisoned:
            self._apply_poison_effect()
            if not self.poison_damage_rounds:
                self.is_poisoned = False

    def attack_with_strength(self, enemy):
        """Performs a physical attack on the target."""
        if enemy.type == "phantom": return
        self._perform_attack(enemy, self.attack_power)

    def attack_with_spirit(self, enemy):
        """Performs a spiritual attack on the target."""
        self._perform_attack(enemy, self.spiritual_power)

    def _perform_attack(self, enemy, attack):
        """Calculates and applies the result of an attack."""
        result_dice = random.randint(1, 20)

        attack += self._apply_weapon_damage(attack)
        efficiency_chance = self.calculate_hit_chance(enemy, attack, result_dice)
        random_factor = random.random()

        if result_dice == 20 or (result_dice != 1 and random_factor <= efficiency_chance):
            self._apply_damage_to_enemy(enemy, attack)
            self._reduce_weapon_durability()
            if enemy.title == "Angry Guardian" and enemy.bonus_attack != 5: enemy.bonus_attack += 1

        self._apply_poison_effect()

    def _apply_poison_effect(self):
        """Applies damage from all active poison effects."""
        if self.poison_damage_rounds:
            # We list the current damage
            total_damage = len(self.poison_damage_rounds)

            self.health_points -= total_damage
            self.check_is_alive()

            # Update rounds counters
            self.damage_rounds = [r - 1 for r in self.poison_damage_rounds if r > 1]

    def _reduce_weapon_durability(self):
        """Reduces weapon durability and marks it as broken if durability reaches zero."""
        if self.weapon:
            self.weapon.durability -= 1
            if self.weapon.durability == 0:
                self.weapon.is_break = True

    def _apply_weapon_damage(self, attack):
        """Applies the weapon's bonus to the attack if it is not broken and used."""
        if self.weapon and not self.weapon.is_break and attack != self.spiritual_power:
            return self.weapon.strike_power
        return 0
