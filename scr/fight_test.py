import json

from creature import Creature


class Fight:
    @staticmethod
    def test_healing():
        mark = Creature("Mark")
        mark.health_points = 90
        print(f"Health points of {mark.title} = {mark.health_points}")

        heal_points = 2
        mark.healing(heal_points)
        print(f"After healing by {heal_points} points: health points of {mark.title} = {mark.health_points}")

        heal_points = 10
        mark.healing(heal_points)
        print(f"After healing by {heal_points} points: health points of {mark.title} = {mark.health_points}")

    @staticmethod
    def test_combat():
        creatures = Fight._load_all_creatures()
        Fight._print_separator()

        creature_1 = Creature(creatures[Fight._select_creature_for_fight(creatures)])
        use_physical_power_1 = Fight._select_attack_type(creature_1)
        Fight._print_separator()

        creature_2 = Creature(creatures[Fight._select_creature_for_fight(creatures)])
        use_physical_power_2 = Fight._select_attack_type(creature_2)
        Fight._print_separator()
        Fight._print_separator()

        fight_rounds = Fight._get_fight_rounds()
        Fight.execute_combat(creature_1, creature_2, use_physical_power_1, use_physical_power_2, fight_rounds)

    @staticmethod
    def execute_combat(creature_1, creature_2, use_physical_power_1, use_physical_power_2, total_rounds):
        round_count = 0
        for _ in range(total_rounds):
            while creature_1.is_alive and creature_2.is_alive:
                round_count += 1
                Fight.perform_attack(creature_1, creature_2, use_physical_power_1)
                if creature_2.is_alive:
                    Fight.perform_attack(creature_2, creature_1, use_physical_power_2)

            if creature_1.is_alive:
                print(f"Rounds {round_count}: {creature_1.title} won!")
            else:
                print(f"Rounds {round_count}: {creature_2.title} won!")

            # /print(
            #     f"Round {round_count}: {creature_1.title} HP={creature_1.health_points}, {creature_2.title} HP={creature_2.health_points}")

            Fight._reset(creature_1)
            Fight._reset(creature_2)
            round_count = 0

    @staticmethod
    def _reset(creature):
        creature.health_points = creature.max_health_points
        creature.is_alive = True

    @staticmethod
    def perform_attack(attacker, defender, use_physical_power):
        if use_physical_power:
            attacker.attack_with_strength(defender)
        else:
            attacker.attack_with_spirit(defender)

    @staticmethod
    def _load_all_creatures():
        try:
            with open("../creatures.json", "r") as file:
                data = json.load(file)
                return Fight._display_creatures(data)
        except FileNotFoundError:
            print("File not found")
            raise
        except json.JSONDecodeError:
            print("Invalid JSON format")
            raise

    @staticmethod
    def _display_creatures(data):
        creatures = []
        for idx, creature in enumerate(data, start=1):
            print(f"{idx}) {creature}")
            creatures.append(creature)
        return creatures

    @staticmethod
    def _select_creature_for_fight(creatures) -> int:
        while True:
            try:
                print("Select a creature by its number: ", end="")
                index = int(input()) - 1
                if 0 <= index < len(creatures):
                    return index
                print("Invalid number. Please select a valid creature number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def _get_fight_rounds():
        while True:
            try:
                attack_count = int(input("Enter the number of fights: "))
                if attack_count > 0:
                    return attack_count
                print("The number of fights must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def _select_attack_type(creature):
        while True:
            try:
                selection = int(input(
                    f"Choose attack type for {creature.title}: --1 Strength ({creature.physical_attack_power}); --2 Spirit ({creature.spiritual_power}): "))
                if selection == 1:
                    return True
                elif selection == 2:
                    return False
                print("Invalid selection. Please choose 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def _print_separator():
        print()
