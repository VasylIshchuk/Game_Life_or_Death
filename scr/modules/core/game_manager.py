from .input_handler import InputHandler
from ..maps.level_manager import LevelManager
from ..maps.level_generator import LevelGenerator

MAX_LEVEL = 5
INITIAL_LEVEL = 1


class GameManager:
    def __init__(self):
        self.open_levels = 0
        self.current_level_number = INITIAL_LEVEL
        self.levels = []
        self.level_manager = None
        self.input_handler = None
        self._run_game()

    def _run_game(self):
        while self.has_closed_levels():
            self.open_next_level()
            self.level_manager.set_current_map()
            self.level_manager.initial_place_hero()
            while self.level_manager.is_current_level_active():
                self.level_manager.display_map()
                self.input_handler.handle_player_action()
                self.level_manager.handle_creatures_action()
                if not self.level_manager.validate_hero_is_alive():
                    self._handle_end_game()
                    return

    def has_closed_levels(self):
        return self.open_levels < MAX_LEVEL

    def open_next_level(self):
        self.open_levels += 1
        level = LevelGenerator(self.current_level_number).generate_level()
        self.level_manager = LevelManager(level)
        self.input_handler = InputHandler(self.level_manager)
        self.levels.append(self.level_manager)

    def set_level(self):
        self.level_manager = self.get_next_level()
        self.input_handler = InputHandler(self.level_manager)

    def get_next_level(self):
        return self.levels[self.current_level_number - 2]

    def _handle_end_game(self):
        print(f"THE END. LOSER!")

    def handle_levels_creatures_action(self):
        """TODO: handle action creature for nex map and previous map"""
        for level_manager in self.levels:
            level_manager.handle_creatures_action()

