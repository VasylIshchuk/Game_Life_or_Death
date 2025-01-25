import json

from ..creatures.creature import Creature
from ..creatures.creature_factory import CreatureFactory

ALLIES_COUNT = 4


def _load_creatures_from_file():
    try:
        with open("./creatures.json", "r") as file:
            data = json.load(file)
            return _filter_and_display_creatures(data)
    except FileNotFoundError:
        print("Error: The file was not found.")
        raise
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        raise


def _filter_and_display_creatures(data):
    creatures = []
    for idx, creature in enumerate(data, start=1):
        if idx > ALLIES_COUNT:
            print(f"{idx - ALLIES_COUNT}) {creature} ")
            creatures.append(creature)
    return creatures


def _select_combat_mode(creatures):
    mode = _get_user_input("Choose combat mode: 1 -- Detailed combat log; 2 -- Statistical summary. Your choice? ", int,
                           1, 2)
    if mode == 1:
        _print_separator()
        _run_detailed_combat_mode(creatures)
    else:
        _print_separator()
        _run_statistical_mode(creatures)


def _run_detailed_combat_mode(creatures):
    creature_1 = CreatureFactory.create_creature("Mark")
    use_spiritual_power = _select_attack_type(creature_1)
    _print_separator()

    creature_2 = _create_creature_from_selection(creatures)
    _print_separator()

    _simulate_detailed_combat(creature_1, creature_2, use_spiritual_power)


def _simulate_detailed_combat(creature_1, creature_2, use_spiritual_power):
    for _ in range(5):
        print("-----------------------------------New Combat-----------------------------------------------------")

        _display_characteristics(creature_1)
        _display_characteristics(creature_2)
        _print_separator()

        _combat_rounds(creature_1, creature_2, use_spiritual_power)

        print("-----------------------------------Combat Finished-----------------------------------------------------")

        _print_separator()
        _print_separator()

        creature_1 = _reset_creature(creature_1)
        creature_2 = _reset_creature(creature_2)


def _combat_rounds(creature_1, creature_2, use_spiritual_power):
    round_count = 0
    while creature_1.is_alive and not creature_1.is_crazy:
        round_count += 1
        print(f"----------Round {round_count}---------")
        if _execute_combat_round(creature_1, creature_2, use_spiritual_power): break
        if _execute_combat_round(creature_2, creature_1): break
        _print_separator()


def _display_characteristics(creature):
    print(
        f"{creature.title} stats: [Category: {creature.category}, HP: {creature.health_points}, Defense: {creature.defense}, Level: {creature.level}, "
        f"Physical Attack: {creature.attack_power}, Agility: {creature.agility}, Abilities: {creature.abilities}]")


def _execute_combat_round(attacker, defender, use_spiritual_power=None):
    health_points_before_attack = defender.health_points
    defense_points_before_attack = defender.get_defense()
    _perform_attack(attacker, defender, use_spiritual_power)
    _display_combat(attacker, defender, health_points_before_attack, defense_points_before_attack)
    if not defender.is_alive:
        print(f"{defender.title} is dead ;(")
        return True
    elif defender.category == "Hero" and defender.is_crazy:
        print(f"{defender.title} went crazy :o")
        return True
    _print_separator()
    return False


def _display_combat(attacker, defender, health_points_before_attack, defense_points_before_attack):
    _show_attack_details(attacker)
    _display_attack_result(attacker, defender, health_points_before_attack, defense_points_before_attack)


def _show_attack_details(creature):
    print(f"{creature.title} attacks...")
    print(f"The {creature.title} has a {round(creature.HIT_CHANCE * 100, 2)}% chance of hitting the enemy.")


def _display_attack_result(attacker, defender, health_points_before_attack, defense_points_before_attack):
    if defender.health_points == health_points_before_attack and defender.get_defense() == defense_points_before_attack:
        print(f"{attacker.title} missed :(")
    else:
        print(f"{attacker.title} hit successfully :)")
        print(f"The {defender.title} lost {health_points_before_attack - defender.health_points} HP.")
        print(f"The {defender.title} has {defender.health_points} HP left.")
        print(f"The {defender.title} has {defender.get_defense()} DP left.")
        if defender.category == "Hero":
            print(f"The {defender.title} has {defender.mental_state} MS left.")


def _run_statistical_mode(creatures):
    creature_1 = CreatureFactory.create_creature("Mark")
    use_spiritual_power = _select_attack_type(creature_1)
    _print_separator()

    creature_2 = _create_creature_from_selection(creatures)
    _print_separator()

    total_combats = _get_combats()
    _print_separator()

    _simulate_statistical_combat(creature_1, creature_2, use_spiritual_power, total_combats)


def _simulate_statistical_combat(creature_1, creature_2, use_spiritual_power, total_combats):
    statistics = {}
    wins_creature_1 = 0
    wins_creature_2 = 0
    for _ in range(total_combats):
        rounds_count = _execute_combat_rounds(creature_1, creature_2, use_spiritual_power)
        _show_combat_result(creature_1, creature_2, rounds_count)

        if creature_1.is_alive:
            wins_creature_1 += 1
        else:
            wins_creature_2 += 1

        statistics[rounds_count] = statistics.get(rounds_count, 0) + 1

        creature_1 = _reset_creature(creature_1)
        creature_2 = _reset_creature(creature_2)

    _show_statistics(statistics, creature_1, creature_2, wins_creature_1, wins_creature_2)
    _print_separator()


def _execute_combat_rounds(creature_1, creature_2, use_spiritual_power):
    rounds_count = 0
    while creature_1.is_alive and not creature_1.is_crazy:
        rounds_count += 1
        _perform_attack(creature_1, creature_2, use_spiritual_power)
        if not creature_2.is_alive: break
        if creature_2.title == "Hero" and creature_2.is_crazy: break
        _perform_attack(creature_2, creature_1)
    return rounds_count


def _show_combat_result(creature_1, creature_2, rounds_count):
    if creature_1.is_alive:
        print(
            f"Rounds {rounds_count}: {creature_1.title} won! {creature_1.title} HP={creature_1.health_points}, {creature_2.title} HP={creature_2.health_points}")
    else:
        print(
            f"Rounds {rounds_count}: {creature_2.title} won! {creature_1.title} HP={creature_1.health_points}, {creature_2.title} HP={creature_2.health_points}")


def _show_statistics(statistics, creature_1, creature_2, wins_creature_1, wins_creature_2):
    _print_separator()
    print("------------------------------------Statistics results---------------------------------------------")
    _show_sorted_statistics(statistics)
    _show_result_creature(creature_1, wins_creature_1, wins_creature_2)
    _show_result_creature(creature_2, wins_creature_2, wins_creature_1)
    print("---------------------------------------------------------------------------------------------------")


def _show_result_creature(creature, wins, loses):
    print(f"\n[ {creature.title} (category: {creature.category}): won: {wins}; lose: {loses} ]\n")


def _show_sorted_statistics(statistics):
    for i in sorted(statistics.keys()):
        print(f"{i}: {statistics[i]}")


def _perform_attack(attacker, defender, use_spiritual_power=None):
    if use_spiritual_power:
        attacker.spiritual_attack(defender)
    else:
        attacker.attack(defender)


def _create_creature_from_selection(creatures):
    selected_index = _get_user_input("Select a creature by its number: ", int, 1, len(creatures)) - 1
    return CreatureFactory.create_creature(creatures[selected_index])


def _select_attack_type(creature):
    return _get_user_input(
        f"Choose attack type for HERO: 1 -- Strength({creature.attack_power}); 2 -- Spirit({creature.spiritual_power}). Your choice? ",
        int, 1, 2) == 2


def _get_combats():
    return _get_user_input("Enter the number of combats: ",
                           int, 1, 100000000)


def _reset_creature(creature):
    return CreatureFactory.create_creature(creature.title)


def _print_separator():
    print()


def _get_user_input(prompt, input_type, min, max):
    while True:
        try:
            user_input = input_type(input(prompt))
            if not min <= user_input <= max:
                print(f"Invalid input. Please choose from [{min}:{max}].")
                _print_separator()
                continue
            return user_input
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            _print_separator()


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
        creatures = _load_creatures_from_file()
        _print_separator()

        _select_combat_mode(creatures)
