import copy
import random

from .tile import Tile
from ..core.icons import Icon
from .grid import Grid
from ..maps.direction import Direction, get_position_toward_direction
from ..maps.position import Position

TILE_ROOM_FLOOR = Tile(Icon.ROOM_FLOOR)
AVAILABLE_TILES = {Icon.ROOM_FLOOR, Icon.GROUND, Icon.CORRIDOR_FLOOR, Icon.WATER, Icon.SWAMP, Icon.CORPSE}
ENTRANCE_POSITION = Position(0, 1)


class Map:
    def __init__(self):
        self.grid = None
        self.creatures = []
        self.items = []
        self.hero = None

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

    def get_creatures(self):
        return self.creatures

    def set_hero(self, hero):
        self.hero = hero

    def is_placement_valid(self, position: Position) -> bool:
        return self._is_position_unoccupied(position)

    def _is_position_unoccupied(self, position):
        return (self._validate_is_entity_position_unoccupied(self.creatures, position) and
                self._validate_is_entity_position_unoccupied(self.items, position) and
                self._validate_is_hero_position_unoccupied(position) and
                self._validate_is_tile_available(position))

    def _validate_is_entity_position_unoccupied(self, entities, position):
        for entity in entities:
            if self._is_place_occupied(entity, position):
                return False
        return True

    def _validate_is_hero_position_unoccupied(self, position):
        if self.hero is not None:
            if self._is_place_occupied(self.hero, position):
                return False
        return True

    def _is_place_occupied(self, entity, position):
        return entity.get_x_position() == position.get_x() and entity.get_y_position() == position.get_y()

    def _validate_is_tile_available(self, position: Position) -> bool:
        return self.get_cell_icon(position) in AVAILABLE_TILES

    def get_item(self, position):
        for item in self.items:
            if self._is_place_occupied(item, position):
                return item
        return None

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

    def _append_creature(self, creature):
        if not self._is_hero(creature) and self._is_new_creature(creature):
            self.creatures.append(creature)

    def _is_new_creature(self, new_creature):
        for creature in self.creatures:
            if creature == new_creature:
                return False
        return True

    def _is_hero(self, creature):
        return creature.title == "Mark"

    def get_exit_position(self):
        return Position(self.get_map_width() - 1, self.get_map_height() - 2)

    def get_entrance_position(self):
        return Position(0, 1)

    def add_entrance(self, icon):
        entrance_position = self.get_entrance_position()
        self.set_cell_icon(entrance_position, icon)

    def add_exit(self):
        exit_position = self.get_exit_position()
        self.set_cell_icon(exit_position, Icon.GATEWAY_EXIT)

    def place_hero_near_entrance(self, hero):
        entrance_position = self.get_entrance_position()
        position = self.get_position_near_entrance(entrance_position)
        self.place_hero(hero, position)

    def place_hero_near_exit(self, hero):
        exit_position = self.get_exit_position()
        position = self.get_position_near_exit(exit_position)
        self.place_hero(hero, position)

    def place_hero(self, hero, position):
        self.place_creature(hero, position)
        self.set_hero(hero)

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
        self.set_cell_icon(creature.get_position(), Icon.CORPSE)
        self.creatures.remove(creature)
        return True

    def get_random_valid_position(self, creature):
        for _ in range(5):
            direction = random.choice(Direction.CARDINAL_DIRECTIONS)
            new_position = get_position_toward_direction(creature.get_position(), direction)
            if self.is_placement_valid(new_position):
                return new_position
        return None

    def print_map(self):
        entity_grid = self._generate_map()
        self._refresh_display()
        print('\n')
        for y in range(entity_grid.height):
            print(
                ''.join(str(entity_grid.get_value(Position(x, y)).icon) for x in range(entity_grid.width)))
        print('\n')

    def _refresh_display(self):
        """TODO: Maybe dont work in Windows"""
        print("\033c", end="")

    def _generate_map(self):
        entity_grid = copy.deepcopy(self.grid)

        for creature in self.creatures:
            self.set_cell(creature, entity_grid)
        for item in self.items:
            self.set_cell(item, entity_grid)

        if self.hero is not None:
            self.set_cell(self.hero, entity_grid)

        return entity_grid

    def set_cell(self, entity, entity_grid):
        cell = entity_grid.get_value(entity.get_position())
        cell.icon = entity.icon
