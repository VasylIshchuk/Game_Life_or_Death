from .level_distributor import LevelCreatureDistributor


class CreatureSpawner:
    def __init__(self, game_level, map):
        self._map = map
        self._game_level = game_level

    def distribution_by_level(self, quantity_main_level_creatures, quantity_lower_level_creatures):
        level_distributor = LevelCreatureDistributor(self._game_level, quantity_main_level_creatures,
                                                     quantity_lower_level_creatures)
        return level_distributor.distribute()


