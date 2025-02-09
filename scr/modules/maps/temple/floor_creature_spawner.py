import random
from ..position import Position
from ...creatures.creature_spawner import CreatureSpawner
from ...creatures.creature_factory import CreatureFactory

MAX_QUANTITY_MAIN_LEVEL_CREATURES = 20
MIN_QUANTITY_LOWER_LEVEL_CREATURE = 15
MAX_CREATURES = 50


class FloorCreatureSpawner(CreatureSpawner):
    def __init__(self, game_level, map):
        super().__init__(game_level, map)
        self.level_distribution = self._get_creature_distribution_by_level()

    def _get_creature_distribution_by_level(self):
        quantity_main_level_creatures = self._calculate_quantity_main_level_creatures()
        quantity_lower_level_creatures = self._calculate_quantity_lower_level_creatures()
        return self.distribution_by_level(quantity_main_level_creatures, quantity_lower_level_creatures)

    def _calculate_quantity_main_level_creatures(self):
        quantity_levels_temple = self._game_level + 2
        return MAX_QUANTITY_MAIN_LEVEL_CREATURES // quantity_levels_temple

    def _calculate_quantity_lower_level_creatures(self):
        quantity_rooms = len(self._map.rooms)
        base_creature_count = self._game_level * (quantity_rooms // 2)
        limited_creature_count = min(base_creature_count, MAX_CREATURES)
        adjusted_creature_count = MIN_QUANTITY_LOWER_LEVEL_CREATURE + quantity_rooms // 3
        return max(limited_creature_count, adjusted_creature_count)

    def spawn_creatures(self):
        available_rooms = self._get_available_rooms()
        for level, count in self.level_distribution.items():
            self._spawn_creatures_with_level(level, count, available_rooms)

    def _get_available_rooms(self):
        return list(self._map.rooms)

    def _spawn_creatures_with_level(self, level, count, available_rooms):
        for _ in range(count):
            creature = CreatureFactory.create_random_creature_by_level(level)
            room = random.choice(available_rooms)
            self._place_creature_in_room(creature, room)

    def _place_creature_in_room(self, creature, room):
        position = self._generate_random_position(room)
        while not self._map.place_creature(creature, position):
            position = self._generate_random_position(room)

    def _generate_random_position(self, room):
        x = random.randint(room.get_x_upper_left_angle() + 2, room.get_x_bottom_right_angle() - 2)
        y = random.randint(room.get_y_upper_left_angle() + 2, room.get_y_bottom_right_angle() - 2)
        return Position(x, y)

