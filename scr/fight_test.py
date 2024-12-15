import json

from creature import Creature

"""Load all creatures from a JSON file"""
def _load_creatures_from_file():
    try:
        with open("../creatures.json", "r") as file:
            data = json.load(file)
            return _display_creatures(data)
    except FileNotFoundError:
        print("Error: The file was not found.")
        raise
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        raise


"""Display the list of creatures and return their details"""
def _display_creatures(data):
    creatures = []
    for idx, creature in enumerate(data, start=1):
        print(f"{idx}) {creature} ")
        creatures.append(creature)
    return creatures


"""Prompt the user to select the combat mode"""
def _select_combat_mode(creatures):
    while True:
        try:
            selection = int(
                input(
                    f"Choose combat mode: 1 -- Detailed combat log; 2 -- Statistical summary. Your choice?  "))
            if selection == 1:
                _print_separator()
                _run_detailed_combat_mode(creatures)
                break
            elif selection == 2:
                _print_separator()
                _run_statistical_mode(creatures)
                break
            print("Invalid selection. Please choose 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a valid number. ")


"""Run combat mode with detailed logs"""
def _run_detailed_combat_mode(creatures):
    creature_1 = _create_creature_from_selection(creatures)
    use_physical_power_1 = _select_attack_type(creature_1)
    _print_separator()

    creature_2 = _create_creature_from_selection(creatures)
    use_physical_power_2 = _select_attack_type(creature_2)
    _print_separator()

    _simulate_detailed_combat(creature_1, creature_2, use_physical_power_1, use_physical_power_2)


"""Simulate detailed combat between two creatures"""
def _simulate_detailed_combat(creature_1, creature_2, use_physical_power_1, use_physical_power_2):
    for _ in range(5):
        print("-----------------------------------New Combat-----------------------------------------------------")

        _display_characteristics(creature_1)
        _display_characteristics(creature_2)
        _print_separator()

        round_count = 0
        while creature_1.is_alive:
            round_count += 1
            print(f"----------Round {round_count}---------")
            if _execute_combat_round(creature_1, creature_2, use_physical_power_1): break
            if _execute_combat_round(creature_2, creature_1, use_physical_power_2): break
            _print_separator()

        print("-----------------------------------Combat Finished-----------------------------------------------------")

        _print_separator()
        _print_separator()

        _reset_creature(creature_1)
        _reset_creature(creature_2)


"""Display creature characteristics"""
def _display_characteristics(creature):
    print(
        f"{creature.title} stats: [Category: {creature.category}, HP: {creature.health_points}, Defense: {creature.defense}, Level: {creature.level}, "
        f"Physical Attack: {creature.physical_attack_power}, Spiritual Power: {creature.spiritual_power}, "
        f"Agility: {creature.agility}]")


"""Execute a single combat round between attacker and defender"""
def _execute_combat_round(attacker, defender, use_physical_power):
    health_points_before_attack = defender.health_points
    _perform_attack(attacker, defender, use_physical_power)
    _show_attack_details(attacker)
    _display_attack_result(attacker, defender, health_points_before_attack)
    if not defender.is_alive:
        print(f"{defender.title} is dead ;(")
        return True
    _print_separator()


"""Displays which creature is attacking and their chance of hitting the enemy"""
def _show_attack_details(creature):
    print(f"{creature.title} attacks...")
    print(f"The {creature.title} has a {round(creature.HIT_CHANCE * 100, 2)}% chance of hitting the enemy.")


"""Display the result of an attack"""
def _display_attack_result(attacker, defender, health_points_before_attack):
    if defender.health_points == health_points_before_attack:
        print(f"{attacker.title} missed :(")
    else:
        print(f"{attacker.title} hit successfully :)")
        print(f"The {defender.title} lost {health_points_before_attack - defender.health_points} HP.")
        print(f"The {defender.title} has {defender.health_points} HP left.")


"""Run combat mode with statistical summary"""
def _run_statistical_mode(creatures):
    creature_1 = _create_creature_from_selection(creatures)
    use_physical_power_1 = _select_attack_type(creature_1)
    _print_separator()

    creature_2 = _create_creature_from_selection(creatures)
    use_physical_power_2 = _select_attack_type(creature_2)
    _print_separator()

    total_combats = _get_combats()
    _print_separator()

    _simulate_statistical_combat(creature_1, creature_2, use_physical_power_1, use_physical_power_2, total_combats)


"""Simulates multiple rounds of combat between two creatures and shows statistics"""
def _simulate_statistical_combat(creature_1, creature_2, use_physical_power_1, use_physical_power_2, total_combats):
    statistics = {}
    wins_creature_1 = 0
    wins_creature_2 = 0
    for _ in range(total_combats):
        rounds_count = _execute_combat_rounds(creature_1, creature_2, use_physical_power_1, use_physical_power_2)
        _show_combat_result(creature_1, creature_2, rounds_count)

        if creature_1.is_alive:
            wins_creature_1 += 1
        else:
            wins_creature_2 += 1

        statistics[rounds_count] = statistics.get(rounds_count, 0) + 1

        _reset_creature(creature_1)
        _reset_creature(creature_2)

    _show_statistics(statistics, creature_1, creature_2, wins_creature_1, wins_creature_2)
    _print_separator()


"""Executes a rounds of combat between two creatures"""
def _execute_combat_rounds(creature_1, creature_2, use_physical_power_1, use_physical_power_2):
    rounds_count = 0
    while creature_1.is_alive:
        rounds_count += 1
        _perform_attack(creature_1, creature_2, use_physical_power_1)
        if not creature_2.is_alive: break
        _perform_attack(creature_2, creature_1, use_physical_power_2)

    return rounds_count


"""Shows the result of each combat (who won and their HPs)"""
def _show_combat_result(creature_1, creature_2, rounds_count):
    if creature_1.is_alive:
        print(
            f"Rounds {rounds_count}: {creature_1.title} won! {creature_1.title} HP={creature_1.health_points}, {creature_2.title} HP={creature_2.health_points}")
    else:
        print(
            f"Rounds {rounds_count}: {creature_2.title} won! {creature_1.title} HP={creature_1.health_points}, {creature_2.title} HP={creature_2.health_points}")


"""Shows the statistics of the combat(frequency of combat ending with the same number of rounds)"""
def _show_statistics(statistics, creature_1, creature_2, wins_creature_1, wins_creature_2):
    _print_separator()
    print("------------------------------------Statistics results---------------------------------------------")
    _show_sorted_statistics(statistics)
    _show_result_creature(creature_1, wins_creature_1, wins_creature_2)
    _show_result_creature(creature_2, wins_creature_2, wins_creature_1)
    print("---------------------------------------------------------------------------------------------------")


""" Shows all rounds, including total wins and losses."""
def _show_result_creature(creature,wins,loses):
    print(f"\n[ {creature.title} (category: {creature.category}): won: {wins}; lose: {loses} ]\n")


"""Sorts and displays round statistics"""
def _show_sorted_statistics(statistics):
    for i in sorted(statistics.keys()):
        print(f"{i}: {statistics[i]}")


"""Performs an attack by the attacker on the defender using either physical power or spiritual power"""
def _perform_attack(attacker, defender, use_physical_power):
    if use_physical_power:
        attacker.attack_with_strength(defender)
    else:
        attacker.attack_with_spirit(defender)


"""Create a creature instance from the user's selection"""
def _create_creature_from_selection(creatures):
    selected_index = _select_creature(creatures)
    return Creature(creatures[selected_index])


"""Prompts the user to select a creature by its index"""
def _select_creature(creatures) -> int:
    while True:
        try:
            print("Select a creature by its number: ", end="")
            index = int(input()) - 1
            if 0 <= index < len(creatures):
                return index
            print("Invalid number. Please select a valid creature number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


"""Prompts the user to select the attack type for a creature"""
def _select_attack_type(creature):
    while True:
        try:
            selection = int(input(
                f"Choose attack type for {creature.title}: 1 -- Strength({creature.physical_attack_power}); 2 -- Spirit({creature.spiritual_power}). Your choice? "))
            if selection == 1:
                return True
            elif selection == 2:
                return False
            print("Invalid selection. Please choose 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


"""Prompts the user to enter the number of combats"""
def _get_combats():
    while True:
        try:
            attack_count = int(input("Enter the number of combats: "))
            if attack_count > 0:
                return attack_count
            print("The number of combats must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


"""Reset a creature's stats after combat"""
def _reset_creature(creature):
    creature.health_points = creature.max_health_points
    creature.is_alive = True


def _print_separator():
    print()


class Fight:
    """Class to manage and test fight scenarios between creatures"""

    """Tests the healing mechanism for a creature by healing a specified number of points"""
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


    """Tests a combat scenario between creatures"""
    @staticmethod
    def test_combat():
        creatures = _load_creatures_from_file()
        _print_separator()

        _select_combat_mode(creatures)