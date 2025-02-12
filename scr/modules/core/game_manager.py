from .input_handler import InputHandler
from ..maps.level_manager import LevelManager
from ..maps.level_generator import LevelGenerator

MAX_LEVEL = 5


class GameManager:
    def __init__(self):
        self.open_levels = 0
        self.current_level_number = 0
        self.levels = []
        self.level_manager = None
        self.input_handler = None
        self._run_game()

    def _run_game(self):
        self.open_next_level()
        self.level_manager.set_current_map()
        self.level_manager.put_hero_near_entrance()

        while self.has_closed_levels():
            self.handle_level()
            while self.level_manager.is_level_in_progress():
                self.level_manager.display_map()
                self.input_handler.handle_player_action()
                self.level_manager.handle_creatures_action()
                if not self.level_manager.validate_hero_is_alive():
                    self._handle_end_game()
                    return

    def has_closed_levels(self):
        return self.open_levels < MAX_LEVEL

    def handle_level(self):
        if self.level_manager.should_move_to_next_level() and self.open_levels == self.current_level_number:
            self.open_next_level()
            self.level_manager.set_current_map()
            self.level_manager.put_hero_near_entrance()
        elif self.level_manager.should_move_to_next_level():
            self.current_level_number += 1
            self.level_manager = self.get_next_level()
            self.set_level()
            self.level_manager.put_hero_near_entrance()
        elif self.level_manager.should_move_to_previous_level():
            self.current_level_number -= 1
            self.level_manager = self.get_previous_level()
            self.set_level()
            self.level_manager.put_hero_near_exit()

    def open_next_level(self):
        self.open_levels += 1
        self.current_level_number += 1
        level = LevelGenerator.generate_level(self.current_level_number)
        self.level_manager = LevelManager(level)
        self.input_handler = InputHandler(self.level_manager)
        self.levels.append(self.level_manager)

    def set_level(self):
        self.level_manager.reset_level_state()
        self.input_handler = InputHandler(self.level_manager)

    def get_next_level(self):
        return self.levels[self.current_level_number - 1]

    def get_previous_level(self):
        return self.levels[self.current_level_number - 1]

    def _handle_end_game(self):
        print(f"THE END. LOSER!")

    def handle_levels_creatures_action(self):
        """TODO: handle action creature for next map and previous map"""
        for level_manager in self.levels:
            level_manager.handle_creatures_action()
