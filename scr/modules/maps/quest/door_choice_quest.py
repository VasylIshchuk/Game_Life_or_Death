from .quest import Quest
from ..position import Position
from ...creatures.creature_factory import CreatureFactory

CREATURE_COUNT = 5


class DoorChoiceQuest(Quest):
    def __init__(self, width=35, height=25, room_half_height=5):
        super().__init__(width, height, room_half_height)
        self._generate_level()

    def place_creatures(self,map_level):
        for _ in range(CREATURE_COUNT):
            creature = CreatureFactory.create_random_creature_by_level(map_level)
            self._place_creature_in_room(creature, 1)

    def _generate_level(self):
        self._generate_choose_room()
        self._generate_quest_room(1, self._y_vertical_wall)
        self._generate_quest_room(self._y_vertical_wall + 1, self._height - 1)

        self._add_doors()
        self._add_information_board()

    def _generate_quest_room(self, start_y, end_y):
        start_x = self._x_horizontal_wall + 1
        start_position = Position(start_x, start_y)

        end_x = self._width - 1
        end_position = Position(end_x, end_y)

        self._generate_room(start_position, end_position)
        self._fill_area(start_position, end_position)

    def _add_doors(self):
        self._add_gateways()
        self._add_quest_doors()

    def _add_gateways(self):
        self._add_entrance(0, self._y_vertical_wall)
        self._add_exit(self._width - 1, self._y_vertical_wall // 2)
        self._add_exit(self._width - 1, self._height - self._y_vertical_wall // 2)

    def _add_quest_doors(self):
        self._add_door(self._x_horizontal_wall, self._y_vertical_wall + 3)
        self._add_door(self._x_horizontal_wall, self._y_vertical_wall - 3)
