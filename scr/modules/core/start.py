from ..creatures.creature_factory import CreatureFactory
from ..maps.direction import Direction, get_position_toward_direction
from ..maps.level_generator import Level
from .render import get_key
from .icons import Icon
from ..maps.temple.temple_generator import TempleGenerator

MAX_LEVEL = 5
INITIAL_LEVEL = 1


class StartGame:
    def __init__(self):
        self.open_levels = 0
        self.current_level = INITIAL_LEVEL
        self.current_floor = 0
        self.levels = []
        self.current_map = None
        self.map = None
        self.hero = CreatureFactory.create_creature("Mark")
        self._start_game()

    def _start_game(self):
        while self._is_close_levels():
            self.open_levels += 1
            level = Level(self.current_level)
            self.levels.append(level)
            self.map = level.get_map()
            self.map.place_hero_near_entrance(self.hero)
            while self.open_levels > self.current_level:
                self.current_map = self.map
                while self.map == self.current_map:
                    self.map.print_map()
                    if self.take_player_decision():
                        break

    def _is_close_levels(self):
        return self.open_levels <= MAX_LEVEL

    def take_player_decision(self):
        action = get_key().lower()

        if action == 'w':
            self.make_move(Direction.NORTH)
        elif action == 's':
            self.make_move(Direction.SOUTH)
        elif action == 'd':
            self.make_move(Direction.EAST)
        elif action == 'a':
            self.make_move(Direction.WEST)
        elif action == 'e':
            self.is_within_range()
        elif action == 'q':
            exit(1)

    def make_move(self, direction):
        new_position = get_position_toward_direction(self.hero.get_position(), direction)
        if self.map.is_placement_valid(new_position):
            self.map.move_creature(self.hero, new_position)

    def is_within_range(self):
        for direction in Direction.CARDINAL_DIRECTIONS:
            new_position = get_position_toward_direction(self.hero.get_position(), direction)
            if self.map.get_cell_icon(new_position) == Icon.GATEWAY_EXIT:
                level = self.get_level()
                level.increase_current_map_index()
                self.map = level.get_map()
                self.map.place_hero_near_entrance(self.hero)
                return True
            elif self.map.get_cell_icon(new_position) == Icon.GATEWAY_ENTRANCE:
                level = self.get_level()
                level.decrease_current_map_index()
                self.map = level.get_map()
                self.map.place_hero_near_exit(self.hero)
                return True
            elif self.map.get_cell_icon(new_position) == Icon.STAIRS:
                self.map = self.choose_floor()
                self.map.put_hero_near_stairs(self.hero)
                return True
        return False

    def get_level(self):
        return self.levels[self.current_level - 1]

    def choose_floor(self):
        if 0 < self.current_floor < self.current_level + 2 - 1:
            print(f"Choose direction:")
            print(f"1 - up")
            print(f"2 - down")

            action = get_key().lower()

            if action == '1':
                return self.get_next_floor_map()
            elif action == '2':
                return self.get_previous_floor_map()

        elif self.current_floor == 0:
            return self.get_next_floor_map()
        elif self.current_floor == self.current_level + 2 -1:
            return self.get_previous_floor_map()

    def get_next_floor_map(self):
        level = self.get_level()
        self.current_floor += 1
        return level.get_floor_map_from_temple(self.current_floor)

    def get_previous_floor_map(self):
        level = self.get_level()
        self.current_floor -= 1
        return level.get_floor_map_from_temple(self.current_floor)
