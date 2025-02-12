import sys
import os
from ..maps.direction import Direction
from .icons import Icon


def get_player_action():
    return get_key().lower()


def get_key():
    if os.name == 'nt':
        return get_windows_key()
    else:
        return get_linux_key()


def get_windows_key():
    import msvcrt
    return msvcrt.getch().decode('utf-8')


def get_linux_key():
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


DIRECTION_ACTION_MAP = {
    'w': Direction.NORTH,
    's': Direction.SOUTH,
    'd': Direction.EAST,
    'a': Direction.WEST
}

TRANSITION_ACTION = ('i', 'o')
ESC_KEY = '\x1b'


class InputHandler:
    def __init__(self, level_manager):
        self.level_manager = level_manager

    def handle_player_action(self):
        # self._prompt_hero_stats()
        while True:
            action = get_player_action()

            if action in DIRECTION_ACTION_MAP:
                direction = DIRECTION_ACTION_MAP[action]
                self.level_manager.move_hero(direction)
                break
            elif action in TRANSITION_ACTION:
                self._handle_transition(action)
                break
            elif action == 't':
                self._open_chest()
                break
            elif action == 'e':
                self.level_manager.handle_attack()
                break
            elif action == 'q':
                self.level_manager.handle_spiritual_attack()
                break
            elif action == 'b':
                self.level_manager.handle_backpack()
                break
            elif action == 'l':
                self.level_manager.handle_book_effect()
                break
            elif action == 'c':
                self.level_manager.handle_food_effect()
                break
            elif action == ESC_KEY:
                print("Exiting...")
                exit(0)

    def _handle_transition(self, action):
        tile_icon = self.level_manager.find_adjacent_transition_tile()
        if tile_icon is not None:
            if action == 'i':
                self.level_manager.handle_transition_level(tile_icon)
            elif action == 'o':
                self.level_manager.handle_transition_map(tile_icon)

    def _open_chest(self):
        chest = self.level_manager.find_adjacent_chest()
        if chest is not None:
            self.level_manager.handle_chest(chest)

    def get_floor_movement_input(self):
        while True:
            action = get_player_action()

            if action == '1':
                return "up"
            elif action == '2':
                return "down"

    def select_item(self, container):
        while True:
            action = get_player_action()

            if action == 'q':
                return None

            if action.isdigit():
                index = int(action) - 1
                if 0 <= index < len(container.get_slots()):
                    return index

    def handle_bacpack_action(self):
        while True:
            action = get_player_action()
            if action == 'u':
                return "Equip"
            elif action == 'd':
                return "Drop"
            elif action == 'e':
                return "Exchange"
            elif action == 's':
                return "Stats"
            if action == 'q':
                return  None

    def _prompt_hero_stats(self):
        stats = {
            "Health Points": self.level_manager.hero.health_points,
            "Mental State": self.level_manager.hero.mental_state,
            "Level": self.level_manager.hero.level,
            "Defense": self.level_manager.hero.get_defense(),
            "Spiritual Power": self.level_manager.hero.spiritual_power,
            "Attack Power": self.level_manager.hero.attack_power,
            "Agility": self.level_manager.hero.agility,
            "Attack Range": self.level_manager.hero.attack_range,
            "Attack Range (Spirit Power)": self.level_manager.hero.attack_range_spirit_power,
            "Experience points": self.level_manager.hero.experience_points
        }

        print("\nHero Stats:")
        for stat, value in stats.items():
            print(f"\t· {stat}: {value}")

        print("\nEquipment:")
        for index in range(self.level_manager.hero.equipment.size):
            item = self.level_manager.hero.equipment.get_item(index)
            if item is None: print(f"\t· {Icon.EMPTY_SLOT}")
            else: print(f"\t· {item.icon} - {item.title} ({item.category})")

