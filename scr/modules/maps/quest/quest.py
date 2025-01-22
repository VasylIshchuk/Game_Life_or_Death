from ..map import Map
from ..position import Position
from ...core.icons import Icon
from ..temple.room import Room


class Quest(Map):
    def __init__(self, width=50, height=30, room_half_height=5):
        super().__init__()
        self.initialize_grid(Icon.GROUND, width, height)
        self.rooms = []

        self._width = width
        self._height = height
        self._choose_room_half_height = room_half_height

        self._x_horizontal_wall = width // 4
        self._y_vertical_wall = height // 2

        self._generate_level()

    def _generate_level(self):
        self._generate_choose_room()
        self._generate_quest_room(1, self._y_vertical_wall)
        self._generate_quest_room(self._y_vertical_wall + 1, self._height - 1)

        self._add_doors()
        self._add_information_board()

    def _generate_choose_room(self):
        start_x = 1
        start_y = self._y_vertical_wall - self._choose_room_half_height
        start_position = Position(start_x, start_y)

        end_x = self._x_horizontal_wall
        end_y = self._y_vertical_wall + self._choose_room_half_height + 1
        end_position = Position(end_x, end_y)

        self._fill_area(start_position, end_position)

    def _generate_quest_room(self, start_y, end_y):
        start_x = self._x_horizontal_wall + 1
        start_position = Position(start_x, start_y)

        end_x = self._width - 1
        end_position = Position(end_x, end_y)

        self._generate_room(start_position, end_position)
        self._fill_area(start_position, end_position)

    def _generate_room(self, start_position, end_position):
        room = Room(self)
        room.width = end_position.get_x() - start_position.get_x()
        room.height = end_position.get_y() - start_position.get_y()
        room.set_coordinates(start_position)
        self.rooms.append(room)

    def _fill_area(self, start_position, end_position):
        for x in range(start_position.get_x(), end_position.get_x()):
            for y in range(start_position.get_y(), end_position.get_y()):
                position = Position(x, y)
                self.set_cell_icon(position, Icon.ROOM_FLOOR)

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

    def _add_door(self, x, y):
        self._add_entity(x, y, Icon.QUEST_DOOR)

    def _add_entrance(self, x, y):
        self._add_entity(x, y, Icon.LEVEL_ENTRANCE)

    def _add_exit(self, x, y):
        self._add_entity(x, y, Icon.LEVEL_ENTRANCE)

    def _add_information_board(self):
        x = self._x_horizontal_wall - 1
        y = self._y_vertical_wall
        self._add_entity(x, y, Icon.INFORMATION_BOARD)

    def _add_entity(self, x, y, icon):
        position = Position(x, y)
        self.set_cell_icon(position, icon)
