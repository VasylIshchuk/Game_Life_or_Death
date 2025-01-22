from .tile import Tile
from .position import Position
from ..core.icons import Icon
from .grid import Grid

TILE_ROOM_FLOOR = Tile(Icon.ROOM_FLOOR)


class Map:
    def __init__(self):
        self.grid = None
        self.creatures = []
        self.items = []
        self.entity_report = []

    def is_item_placement_valid(self, position: Position) -> bool:
        return self.get_cell_icon(position) == Icon.ROOM_FLOOR

    def is_creature_placement_valid(self, position: Position) -> bool:
        return self.get_cell_icon(position) == Icon.ROOM_FLOOR

    def get_cell_icon(self, position):
        cell = self.grid.get_value(position)
        return cell.icon

    def place_hero_start_position(self, hero):
        start_position = Position(1, 1)
        tile_creature = Tile(hero.icon)
        self.grid.set_value(start_position, tile_creature)
        hero.set_position(start_position)
        self.creatures.append(hero)
        self.entity_report.append(hero)

    def place_item(self, item, position: Position) -> bool:
        if self.is_item_placement_valid(position):
            tile_item = Tile(item.icon)
            self.grid.set_value(position, tile_item)
            item.set_position(position)
            self.items.append(item)
            self.entity_report.append(item)
            return True
        return False

    def place_creature(self, creature, position: Position) -> bool:
        if self.is_creature_placement_valid(position):
            tile_creature = Tile(creature.icon)
            self.grid.set_value(position, tile_creature)
            creature.set_position(position)
            self.creatures.append(creature)
            self.entity_report.append(creature)
            return True
        return False

    def remove_item(self, position: Position) -> bool:
        item = self._find_item(position)
        if item:
            self.grid.set_value(position, TILE_ROOM_FLOOR)
            item.set_position(Position(None, None))
            self.entity_report.remove(item)
            return True
        return False

    def _find_item(self, position: Position):
        for entity in self.items:
            if entity.position == position:
                return entity
        return None

    def remove_creature(self, position: Position) -> bool:
        creature = self._find_creature(position)
        if creature:
            self.grid.set_value(position, TILE_ROOM_FLOOR)
            creature.set_position(Position(None, None))
            self.entity_report.remove(creature)
            return True
        return False

    def _find_creature(self, position: Position):
        for creature in self.creatures:
            if creature.position == position:
                return creature
        return None

    def initialize_grid(self, icon, width, height):
        tile = Tile(icon)
        self.grid = Grid(tile, width, height)

    def set_cell_icon(self, position, icon):
        cell = self.grid.get_value(position)
        cell.icon = icon

    def get_map_width(self):
        return self.grid.get_width()

    def get_map_height(self):
        return self.grid.get_height()

    def print_map(self):
        print('\n')
        for y in range(self.grid.height):
            print(
                ''.join(str(self.grid.get_value(Position(x, y)).icon) for x in range(self.grid.width)))
        print('\n')

    def generate_report(self):
        for entity in self.entity_report:
            print(
                f"{type(entity).__name__} -> title: {entity.title}; icon: {entity.icon};"
                f"position: x = {entity.position.x} y = {entity.position.y}")
