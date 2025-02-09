import copy
import random

from .tile import Tile
from ..core.icons import Icon
from .grid import Grid
from ..maps.direction import Direction, get_position_toward_direction
from ..maps.position import Position

TILE_ROOM_FLOOR = Tile(Icon.ROOM_FLOOR)
AVAILABLE_TILES = {Icon.ROOM_FLOOR, Icon.GROUND, Icon.CORRIDOR_FLOOR}
ENTRANCE_POSITION = Position(0, 1)


class Map:
    def __init__(self):
        self.grid = None
        self.creatures = []
        self.items = []

    def is_placement_valid(self, position: Position) -> bool:
        return self.get_cell_icon(position) in AVAILABLE_TILES

    def place_item(self, item, position: Position) -> bool:
        if self.is_placement_valid(position):
            item.set_position(position)
            self.items.append(item)
            return True
        return False

    def place_creature(self, creature, position: Position) -> bool:
        if self.is_placement_valid(position):
            creature.set_position(position)
            self._append_creature(creature)
            return True
        return False

    def move_creature(self, creature, position: Position):
        self.place_creature(creature, position)

    def _append_creature(self, creature):
        if self._is_new_creature(creature):
            self.creatures.append(creature)

    def _is_new_creature(self, new_creature):
        for creature in self.creatures:
            if creature == new_creature:
                return False
        return True

    def _is_hero(self, creature):
        return creature.title == "Mark"

    def place_hero_near_entrance(self, hero):
        entrance_position = self.get_entrance_position()
        position = self.get_position_near_entrance(entrance_position)
        self.place_creature(hero, position)

    def place_hero_near_exit(self, hero):
        exit_position = self.get_exit_position()
        position = self.get_position_near_exit(exit_position)
        self.place_creature(hero, position)

    def get_position_near_entrance(self, entrance_position):
        x = entrance_position.get_x() + 1
        y = self._get_y(entrance_position)
        return Position(x, y)

    def get_position_near_exit(self, entrance_position):
        x = entrance_position.get_x() - 1
        y = self._get_y(entrance_position)
        return Position(x, y)

    def _get_y(self, entrance_position):
        return entrance_position.get_y()

    def remove_creature(self, creature) -> bool:
        self.grid.set_value(creature.get_position(), Tile(Icon.CORPSE))
        self.creatures.remove(creature)
        return True

    def get_random_valid_position(self, creature):
        for _ in range(5):
            direction = random.choice(Direction.CARDINAL_DIRECTIONS)
            new_position = get_position_toward_direction(creature, direction)
            if self.is_placement_valid(new_position):
                return new_position
        return None

    def initialize_grid(self, icon, width, height):
        tile = Tile(icon)
        self.grid = Grid(tile, width, height)

    def get_cell_icon(self, position):
        cell = self.grid.get_value(position)
        return cell.icon

    def set_cell_icon(self, position, icon):
        cell = self.grid.get_value(position)
        cell.icon = icon

    def get_map_width(self):
        return self.grid.get_width()

    def get_map_height(self):
        return self.grid.get_height()

    def get_exit_position(self):
        return Position(self.get_map_width() - 1, self.get_map_height() - 2)

    def get_entrance_position(self):
        return Position(0, 1)

    def add_gateways(self):
        self.add_entrance(Icon.GATEWAY_ENTRANCE)
        self.add_exit(Icon.GATEWAY_EXIT)

    def add_entrance(self, icon):
        entrance_position = self.get_entrance_position()
        self.set_cell_icon(entrance_position, icon)

    def add_exit(self, icon):
        exit_position = self.get_exit_position()
        self.set_cell_icon(exit_position, icon)

    def print_map(self):
        entity_grid = self.generate_map()
        print('\n')
        for y in range(entity_grid.height):
            print(
                ''.join(str(entity_grid.get_value(Position(x, y)).icon) for x in range(entity_grid.width)))
        print('\n')

    def generate_map(self):
        entity_grid = copy.deepcopy(self.grid)

        for creature in self.creatures:
            self.set_cell(creature, entity_grid)
        for item in self.items:
            self.set_cell(item, entity_grid)

        return entity_grid

    def set_cell(self, entity, entity_grid):
        cell = entity_grid.get_value(entity.get_position())
        cell.icon = entity.icon
