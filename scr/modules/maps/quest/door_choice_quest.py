from .quest import Quest
from ..position import Position
from ...creatures.creature_factory import CreatureFactory
from ...core.icons import Icon

CREATURE_COUNT = 5


class DoorChoiceQuest(Quest):
    def __init__(self, width=40, height=30, room_half_height=5):
        super().__init__(width, height, room_half_height)
        self._generate_level()
        self._is_selected_first_quest_room = False

    def place_hero_near_exit(self, hero):
        if self._is_selected_first_quest_room:
            position = self.get_first_quest_room_exit_position()
        else:
            position = self.get_second_quest_room_exit_position()
        self.place_hero(hero, position)

    def place_creatures(self, map_level):
        for _ in range(CREATURE_COUNT):
            creature = CreatureFactory.create_random_creature_by_level(map_level)
            self.place_creature_in_room(creature, 1)

    def closed_quest_room(self, door_position):
        self._place_entity(door_position, Icon.CLOSED_LEVEL_EXIT)
        first_quest_room_door_position = self.get_first_quest_room_door_position()
        if door_position.get_x() == first_quest_room_door_position.get_x() and door_position.get_y() == first_quest_room_door_position.get_y():
            self._is_selected_first_quest_room = True

    def open_quest_room(self):
        if self._is_selected_first_quest_room:
            self._place_entity(self.get_first_quest_room_door_position(), Icon.DOOR)
            self._place_entity(self.get_first_quest_room_exit_position(), Icon.LEVEL_EXIT)
        else:
            self._place_entity(self.get_second_quest_room_door_position(), Icon.DOOR)
            self._place_entity(self.get_second_quest_room_exit_position(), Icon.LEVEL_EXIT)

    def is_completed_quest(self):
        index = 0 if self._is_selected_first_quest_room else 1
        return self.is_room_cleared(index)

    def get_first_quest_room_door_position(self):
        return Position(self._x_horizontal_wall, self._y_vertical_wall - 4)

    def get_second_quest_room_door_position(self):
        return Position(self._x_horizontal_wall, self._y_vertical_wall + 4)

    def get_first_quest_room_exit_position(self):
        return Position(self._width - 1, self._y_vertical_wall // 2)

    def get_second_quest_room_exit_position(self):
        return Position(self._width - 1, self._height - self._y_vertical_wall // 2)

    def _generate_level(self):
        self.generate_choose_room()
        self._generate_quest_room(1, self._y_vertical_wall - 2)
        self._generate_quest_room(self._y_vertical_wall + 3, self._height - 1)

        self._add_doors()
        self.place_information_board()

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
        self.place_entrance(self.get_entrance_position())
        self.place_exit(self.get_first_quest_room_exit_position())
        self.place_exit(self.get_second_quest_room_exit_position())

    def _add_quest_doors(self):
        self.place_door(self.get_first_quest_room_door_position())
        self.place_door(self.get_second_quest_room_door_position())
