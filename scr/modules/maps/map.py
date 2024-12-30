from .tile import Tile
from .position import Position


class Map:
    def __init__(self):
        self.grid = None
        self.creatures = []
        self.items = []
        self.entity_report = []

    def is_item_placement_valid(self, position: Position) -> bool:
        return self.grid.get(position).icon == Tile.ROOM_FLOOR

    def is_creature_placement_valid(self, position: Position) -> bool:
        return self.grid.get(position).icon == Tile.ROOM_FLOOR

    def place_item(self, item, position: Position) -> bool:
        if self.is_item_placement_valid(position):
            self.grid.set(position, Tile(item.icon))
            item.set_position(position)
            self.items.append(item)
            self.entity_report.append(item)
            return True
        return False

    def place_creature(self, creature, position: Position) -> bool:
        if self.is_creature_placement_valid(position):
            self.grid.set(position, Tile(creature.icon))
            creature.set_position(position)
            self.creatures.append(creature)
            self.entity_report.append(creature)
            return True
        return False

    def remove_item(self, position: Position) -> bool:
        item = self._find_item(position)
        if item:
            self.grid.set(position, Tile(Tile.ROOM_FLOOR))
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
            self.grid.set(position, Tile(Tile.ROOM_FLOOR))
            creature.set_position(Position(None, None))
            self.entity_report.remove(creature)
            return True
        return False

    def _find_creature(self, position: Position):
        for creature in self.creatures:
            if creature.position == position:
                return creature
        return None

    def print_map(self):
        print('\n')
        for y in range(self.grid.height):
            print(
                ''.join(str(self.grid.get(Position(x, y)).icon) for x in range(self.grid.width)))
        print('\n')

    def generate_report(self):
        for entity in self.entity_report:
            print(
                f"{type(entity).__name__} -> title: {entity.title}; icon: {entity.icon};"
                f"position: x = {entity.position.x} y = {entity.position.y}")
