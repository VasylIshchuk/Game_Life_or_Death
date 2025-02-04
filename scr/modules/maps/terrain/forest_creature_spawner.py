import random
from ..position import Position
from ...creatures.creature_spawner import CreatureSpawner
from ...creatures.creature_factory import CreatureFactory

MAX_QUANTITY_MAIN_LEVEL_CREATURES = 5
COEFFICIENT_NUMBER_OF_LOWER_LEVEL_CREATURE = 15


class ForestCreatureSpawner(CreatureSpawner):
    def __init__(self, game_level, map):
        super().__init__(game_level, map)
        self.level_distribution = self._get_creature_distribution_by_level()

    def _get_creature_distribution_by_level(self):
        quantity_lower_level_creatures = self._calculate_quantity_lower_level_creatures()
        return self.distribution_by_level(MAX_QUANTITY_MAIN_LEVEL_CREATURES, quantity_lower_level_creatures)

    def _calculate_quantity_lower_level_creatures(self):
        return self._game_level * COEFFICIENT_NUMBER_OF_LOWER_LEVEL_CREATURE

    def spawn_creatures(self):
        for level, count in self.level_distribution.items():
            for _ in range(count):
                creature = CreatureFactory.create_random_creature_by_level(level)
                self._place_creature_in_forest(creature)

    def _place_creature_in_forest(self, creature):
        position = self._generate_random_position()
        while not self._map.place_creature(creature, position):
            position = self._generate_random_position()

    def _generate_random_position(self):
        x = random.randint(1, self._map.get_map_width() - 2)
        y = random.randint(1, self._map.get_map_height() - 2)
        return Position(x, y)
