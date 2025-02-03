from .quest import Quest
from ..position import Position


class ChamberQuest(Quest):
    def __init__(self,width=25, height=15, room_half_height=4):
        super().__init__(width,height, room_half_height)
        self._generate_level()

    def get_center_room_position(self):
        upper_left_angle = self.get_room_upper_left_angle(0)
        bottom_right_angle = self.get_room_bottom_right_angle(0)
        center_x = (upper_left_angle.get_x() + bottom_right_angle.get_x()) // 2
        center_y = (upper_left_angle.get_y() + bottom_right_angle.get_y()) // 2
        return Position(center_x, center_y)

    def _generate_level(self):
        self._generate_choose_room()
        self._generate_quest_room()

        self._add_doors()
        self._add_information_board()

    def _generate_quest_room(self):
        start_x = self._x_horizontal_wall + 1
        start_y = self._y_vertical_wall - self._choose_room_half_height
        start_position = Position(start_x, start_y)

        end_x = self._width - 1
        end_y = self._y_vertical_wall + self._choose_room_half_height + 1
        end_position = Position(end_x, end_y)

        self._generate_room(start_position, end_position)
        self._fill_area(start_position, end_position)

    def _add_doors(self):
        self._add_gateways()
        self._add_quest_door()

    def _add_gateways(self):
        self._add_entrance(0, self._y_vertical_wall)
        self._add_exit(self._width - 1, self._y_vertical_wall)

    def _add_quest_door(self):
        self._add_door(self._x_horizontal_wall, self._y_vertical_wall)


