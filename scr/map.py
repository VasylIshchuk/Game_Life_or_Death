from item import Item
from creature import Creature
from tile import Tile
from position import Position


class Map:

    def __init__(self):
        self.grid = []
        self.load_map()
        self.creatures = []
        self.items = []
        self.entity_report = []

    # Loads map data from a file and sends it for processing
    def load_map(self):
        try:
            with open('../map_layout.txt', 'r') as file:
                self.parse_layout(file.read())
        except FileNotFoundError:
            print("File not found")
            raise

    # Converts the text content of the file into a grid (map)
    def parse_layout(self, file):
        lines = file.splitlines()
        for line in lines:
            row = []
            for elem in line:
                row.append(Tile(elem))
            self.grid.append(row)

    # Checks if an item can be placed at the given position
    def is_item_placement_valid(self, position: Position) -> bool:
        return self.grid[position.x][position.y].element == Tile.FLOOR

    # Checks if a creature can be placed at the given position
    def is_creature_placement_valid(self, position: Position) -> bool:
        return self.grid[position.x][position.y].element == Tile.FLOOR

    # Places an item at the specified position on the map
    def place_item(self, item: Item, position: Position) -> bool:
        if self.is_item_placement_valid(position):
            self.grid[position.x][position.y] = Tile(item.icon)
            item.set_position(position)
            self.items.append(item)
            self.entity_report.append(item)
            return True
        return False

    # Places a creature at the specified position on the map
    def place_creature(self, creature: Creature, position: Position) -> bool:
        if self.is_creature_placement_valid(position):
            self.grid[position.x][position.y] = Tile(creature.icon)
            creature.set_position(position)
            self.creatures.append(creature)
            self.entity_report.append(creature)
            return True
        return False

    # Removes an item from the specified position
    def remove_item(self, position: Position) -> bool:
        item = self._find_item(position)
        if item:
            self.grid[position.x][position.y] = Tile(Tile.FLOOR)
            item.set_position(Position(None, None))
            self.entity_report.remove(item)
            return True
        return False

    # Finds an item by its position
    def _find_item(self, position: Position):
        for entity in self.items:
            if entity.position == position:
                return entity
        return None

    # Removes a creature from the specified position
    def remove_creature(self, position: Position) -> bool:
        creature = self._find_creature(position)
        if creature:
            self.grid[position.x][position.y] = Tile(Tile.FLOOR)
            creature.set_position(Position(None, None))
            self.entity_report.remove(creature)
            return True
        return False

    # Finds a creature by its position
    def _find_creature(self, position: Position):
        for creature in self.creatures:
            if creature.position == position:
                return creature
        return None

    # Generates a report of all entities on the map
    def generate_report(self):
        for entity in self.entity_report:
            print(
                f"{type(entity).__name__} -> title: {entity.title}; icon: {entity.icon}; description: {entity.description}; "
                f"position: x = {entity.position.x} y = {entity.position.y}")