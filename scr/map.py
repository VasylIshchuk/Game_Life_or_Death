from item import *
from creature import *
from tile import *


class Map:

    def __init__(self):
        self.grid = []
        self.load_map()
        self.creatures = []
        self.entity_report = []

    # Loads map data from a file and sends it for processing
    def load_map(self):
        try:
            with open('map_layout.txt', 'r') as file:
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
    def remove_item(self, item: Item, position: Position) -> bool:
        if self.grid[position.x][position.y].element == item.icon:
            self.grid[position.x][position.y] = Tile(Tile.FLOOR)
            self.entity_report.remove(item)
            return True
        return False

    # Removes a creature from the specified position
    def remove_creature(self, creature: Creature, position: Position) -> bool:
        if self.grid[position.x][position.y].element == creature.icon:
            self.grid[position.x][position.y] = Tile(Tile.FLOOR)
            creature.set_position(Position(None, None))
            self.entity_report.remove(creature)
            return True
        return False

    def generate_report(self):
        for entity in self.entity_report:
            print(
                f"{type(entity).__name__} -> title: {entity.title}; icon: {entity.icon}; description: {entity.description}; "
                f"position: x = {entity.position.x} y = {entity.position.y}")
