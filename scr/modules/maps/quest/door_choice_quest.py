from .quest import Quest
from ..position import Position
from ...creatures.creature_factory import CreatureFactory

CREATURE_COUNT = 5


class DoorChoiceQuest(Quest):
    def __init__(self, width=35, height=25, room_half_height=5):
        super().__init__(width, height, room_half_height)
        self._generate_level()

    def place_hero_near_exit(self, hero):
        """TODO: you must change self.get_exit_position() in one of get_first_quest_room_door_position..."""
        exit_position = self.get_exit_position()
        position = self.get_position_near_exit(exit_position)
        self.place_creature(hero, position)

    def place_creatures(self, map_level):
        for _ in range(CREATURE_COUNT):
            creature = CreatureFactory.create_random_creature_by_level(map_level)
            self.place_creature_in_room(creature, 1)

    def get_first_quest_room_door_position(self):
        return Position(self._x_horizontal_wall, self._y_vertical_wall + 3)

    def get_second_quest_room_door_position(self):
        return Position(self._x_horizontal_wall, self._y_vertical_wall - 3)

    def get_first_quest_room_exit_position(self):
        return Position(self._width - 1, self._y_vertical_wall // 2)

    def get_second_quest_room_exit_position(self):
        return Position(self._width - 1, self._height - self._y_vertical_wall // 2)

    def _generate_level(self):
        self.generate_choose_room()
        self._generate_quest_room(1, self._y_vertical_wall)
        self._generate_quest_room(self._y_vertical_wall + 1, self._height - 1)

        self._add_doors()
        self.add_information_board()

    def _generate_quest_room(self, start_y, end_y):
        start_x = self._x_horizontal_wall + 1
        start_position = Position(start_x, start_y)

        end_x = self._width - 1
        end_position = Position(end_x, end_y)

        self.generate_room(start_position, end_position)
        self.fill_area(start_position, end_position)

    def _add_doors(self):
        self._add_gateways()
        self._add_quest_doors()

    def _add_gateways(self):
        self.add_entrance(self.get_entrance_position())
        self.add_exit(self.get_first_quest_room_exit_position())
        self.add_exit(self.get_second_quest_room_exit_position())

    def _add_quest_doors(self):
        self.add_door(self.get_first_quest_room_door_position())
        self.add_door(self.get_second_quest_room_door_position())
