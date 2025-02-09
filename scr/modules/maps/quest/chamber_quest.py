from .quest import Quest
from ..position import Position


class ChamberQuest(Quest):
    def __init__(self, width=25, height=11, room_half_height=4):
        super().__init__(width, height, room_half_height)
        self._generate_level()

    def place_hero_near_exit(self, hero):
        exit_position = self.get_exit_position()
        position = self.get_position_near_exit(exit_position)
        self.place_creature(hero, position)

    def get_center_room_position(self):
        upper_left_angle = self.get_room_upper_left_angle(0)
        bottom_right_angle = self.get_room_bottom_right_angle(0)
        center_x = (upper_left_angle.get_x() + bottom_right_angle.get_x()) // 2
        center_y = (upper_left_angle.get_y() + bottom_right_angle.get_y()) // 2
        return Position(center_x, center_y)

    def get_exit_position(self):
        return Position(self._width - 1, self._y_vertical_wall)

    def get_quest_door_position(self):
        return Position(self._x_horizontal_wall, self._y_vertical_wall)

    def _generate_level(self):
        self.generate_choose_room()
        self._generate_quest_room()

        self._add_doors()
        self.add_information_board()

    def _generate_quest_room(self):
        start_x = self._x_horizontal_wall + 1
        start_y = 1
        start_position = Position(start_x, start_y)

        end_x = self._width - 1
        end_y = self._height - 1
        end_position = Position(end_x, end_y)

        self.generate_room(start_position, end_position)
        self.fill_area(start_position, end_position)

    def _add_doors(self):
        self._add_gateways()
        self._add_quest_door()

    def _add_gateways(self):
        self.add_entrance(self.get_entrance_position())
        self.add_exit(self.get_exit_position())

    def _add_quest_door(self):
        self.add_door(self.get_quest_door_position())
