# Run tests from the terminal:
# python -m unittest -v test_map.py

import unittest
from ..maps.temple.temple import Temple
from ..items.item_factory import ItemFactory
from ..creatures.creature_factory import CreatureFactory
from ..maps.position import Position


class TestMap(unittest.TestCase):
    def setUp(self):
        self.map = Temple(21, 17)
        self.valid_position = Position(self.map.rooms[0].upper_left_angle.x, self.map.rooms[0].upper_left_angle.y)
        self.invalid_position = Position(self.map.rooms[0].upper_left_angle.x - 1, self.map.rooms[0].upper_left_angle.y)
        self.item = ItemFactory.create_item('Spear')
        self.creature = CreatureFactory.create_creature('Shadow')

    def test_load_map(self):
        self.map.print_map()

    def test_is_item_placement_valid(self):
        assert (self.map.is_item_placement_valid(self.valid_position) == True)
        assert (self.map.is_item_placement_valid(self.invalid_position) == False)

    def test_is_creature_placement_valid(self):
        assert (self.map.is_item_placement_valid(self.valid_position) == True)
        assert (self.map.is_item_placement_valid(self.invalid_position) == False)

    def test_place_item_success(self):
        assert (self.map.place_item(self.item, self.valid_position) == True)

    def test_place_item_failure(self):
        assert (self.map.place_item(self.item, self.invalid_position) == False)

    def test_place_creature_success(self):
        assert (self.map.place_creature(self.creature, self.valid_position) == True)

    def test_place_creature_failure(self):
        assert (self.map.place_creature(self.creature, self.invalid_position) == False)

    def test_remove_item_success(self):
        self.map.place_item(self.item, self.valid_position)
        assert (self.map.remove_item(self.valid_position) == True)

    def test_remove_item_failure(self):
        self.map.place_item(self.item, self.valid_position)
        assert (self.map.remove_item(self.invalid_position) == False)

    def test_remove_creature_success(self):
        self.map.place_creature(self.creature, self.valid_position)
        assert (self.map.remove_creature(self.valid_position) == True)

    def test_remove_creature_failure(self):
        self.map.place_creature(self.creature, self.valid_position)
        assert (self.map.remove_creature(self.invalid_position) == False)

    def test_generate_report(self):
        self.map.place_item(self.item, self.valid_position)
        valid_position = Position(self.map.rooms[0].upper_left_angle.x, self.map.rooms[0].upper_left_angle.y)
        self.map.place_creature(self.creature, valid_position)
        self.map.generate_report()


if __name__ == "__main__":
    unittest.main()
