import random

from ..map import Map
from ..position import Position
from ..temple.room import Room
from ...core.icons import Icon


class Quest(Map):
    def __init__(self, width, height, room_half_height):
        super().__init__()
        self.initialize_grid(Icon.WALL, width, height)
        self.rooms = []

        self._width = width
        self._height = height
        self._choose_room_half_height = room_half_height

        self._x_horizontal_wall = width // 4
        self._y_vertical_wall = height // 2

    def is_room_cleared(self, index):
        room_upper_left_angle_position = self.get_room_upper_left_angle_position(index)
        room_bottom_right_position = self.get_room_bottom_right_angle_position(index)
        for creature in self.creatures:
            creature_x = creature.get_x_position()
            creature_y = creature.get_y_position()
            if (room_upper_left_angle_position.get_x() <= creature_x <= room_bottom_right_position.get_x()
                    and room_upper_left_angle_position.get_y() <= creature_y <= room_bottom_right_position.get_y()):
                return False
        return True

    def place_hero_near_entrance(self, hero):
        entrance_position = self.get_entrance_position()
        position = self.get_position_near_entrance(entrance_position)
        self.place_hero(hero, position)

    def get_room_upper_left_angle_position(self, index):
        x = self.rooms[index].get_x_upper_left_angle()
        y = self.rooms[index].get_y_upper_left_angle()
        return Position(x, y)

    def get_room_bottom_right_angle_position(self, index):
        x = self.rooms[index].get_x_bottom_right_angle()
        y = self.rooms[index].get_y_bottom_right_angle()
        return Position(x, y)

    def get_entrance_position(self):
        return Position(0, self._y_vertical_wall)

    def place_creature_in_room(self, creature, index_room):
        position = self._generate_random_position(index_room)
        while not self.place_creature(creature, position):
            position = self._generate_random_position(index_room)

    def place_item_in_room(self, item, index_room):
        position = self._generate_random_position(index_room)
        while not self.place_item(item, position):
            position = self._generate_random_position(index_room)

    def _generate_random_position(self, index_room):
        upper_left_angle = self.get_room_upper_left_angle_position(index_room)
        bottom_right_angle = self.get_room_bottom_right_angle_position(index_room)
        x = random.randint(upper_left_angle.get_x() + 1, bottom_right_angle.get_x() - 2)
        y = random.randint(upper_left_angle.get_y() + 1, bottom_right_angle.get_y())
        return Position(x, y)

    def generate_choose_room(self):
        start_x = 1
        start_y = self._y_vertical_wall - self._choose_room_half_height
        start_position = Position(start_x, start_y)

        end_x = self._x_horizontal_wall
        end_y = self._y_vertical_wall + self._choose_room_half_height + 1
        end_position = Position(end_x, end_y)

        self.fill_area(start_position, end_position, Icon.CORRIDOR_FLOOR)

    def generate_room(self, start_position, end_position):
        room = Room(self)
        room.width = end_position.get_x() - start_position.get_x()
        room.height = end_position.get_y() - start_position.get_y()
        room.set_coordinates(start_position)
        self.rooms.append(room)

    def fill_area(self, start_position, end_position, icon=Icon.ROOM_FLOOR):
        for x in range(start_position.get_x(), end_position.get_x()):
            for y in range(start_position.get_y(), end_position.get_y()):
                position = Position(x, y)
                self.set_cell_icon(position, icon)

    def place_door(self, position):
        self._place_entity(position, Icon.QUEST_DOOR)

    def place_entrance(self, position):
        self._place_entity(position, Icon.GATEWAY_ENTRANCE)

    def place_exit(self, position):
        self._place_entity(position, Icon.CLOSED_LEVEL_EXIT)

    def place_information_board(self):
        x = self._x_horizontal_wall // 2
        y = self._y_vertical_wall + self._choose_room_half_height
        position = Position(x, y)
        self._place_entity(position, Icon.INFORMATION_BOARD)

    def _place_entity(self, position, icon):
        self.set_cell_icon(position, icon)
