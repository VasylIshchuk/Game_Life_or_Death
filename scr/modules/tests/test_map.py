# Run tests from the terminal:
# python -m unittest -v test_map.py

import unittest
from ..map.map import Map
from ..core.item_factory import ItemFactory
from ..core.creature_factory import CreatureFactory
from ..map.position import Position


def print_map(map):
    print('\n')
    for row in map.grid:
        print(''.join(elem.icon for elem in row))
    print('\n')


class TestMap(unittest.TestCase):
    def setUp(self):
        self.map = Map()
        self.item = ItemFactory.create_item('Spear')
        self.creature = CreatureFactory.create_creature('Mark')

    def test_load_map(self):
        print_map(self.map)

    def test_is_item_placement_valid(self):
        assert (self.map.is_item_placement_valid(Position(4, 30)) == True)
        assert (self.map.is_item_placement_valid(Position(2, 40)) == False)

    def test_is_creature_placement_valid(self):
        assert (self.map.is_item_placement_valid(Position(4, 30)) == True)
        assert (self.map.is_item_placement_valid(Position(2, 40)) == False)

    def test_place_item_success(self):
        print_map(self.map)
        assert (self.map.place_item(self.item, Position(6, 15)) == True)
        print_map(self.map)

    def test_place_item_failure(self):
        print_map(self.map)
        assert (self.map.place_item(self.item, Position(9, 60)) == False)
        print_map(self.map)

    def test_place_creature_success(self):
        print_map(self.map)
        assert (self.map.place_creature(self.creature, Position(7, 8)) == True)
        print_map(self.map)

    def test_place_creature_failure(self):
        print_map(self.map)

        assert (self.map.place_creature(self.creature, Position(3, 60)) == False)
        print_map(self.map)

    def test_remove_item_success(self):
        position = Position(7, 8)
        self.map.place_item(self.item, position)
        print_map(self.map)

        assert (self.map.remove_item(position) == True)
        print_map(self.map)

    def test_remove_item_failure(self):
        position = Position(7, 8)
        self.map.place_item(self.item, position)
        print_map(self.map)

        position = Position(9, 2)
        assert (self.map.remove_item(position) == False)
        print_map(self.map)

    def test_remove_creature_success(self):
        position = Position(3, 25)
        self.map.place_creature(self.creature, position)
        print_map(self.map)

        assert (self.map.remove_creature(position) == True)
        print_map(self.map)

    def test_remove_creature_failure(self):
        position = Position(3, 25)
        self.map.place_creature(self.creature, position)
        print_map(self.map)

        position = Position(3, 50)
        assert (self.map.remove_creature(position) == False)
        print_map(self.map)

    def test_generate_report(self):
        self.map.place_item(self.item, Position(6, 15))
        self.map.place_creature(self.creature, Position(7, 8))
        print('\n')
        self.map.generate_report()
        print('\n')


if __name__ == "__main__":
    unittest.main()
