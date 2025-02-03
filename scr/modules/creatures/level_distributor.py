class LevelCreatureDistributor:
    def __init__(self, game_level, quantity_main_level_creatures, quantity_lower_level_creatures):
        self._game_level = game_level
        self.quantity_main_level_creatures = quantity_main_level_creatures
        self.quantity_lower_level_creatures = quantity_lower_level_creatures
        self._levels = list()
        self._weights = []

    def distribute(self):
        self._levels = self._get_available_levels()
        self._weights = self._calculate_weights()
        total_weight = sum(self._weights)

        lower_distribution = self._calculate_quantity_creatures_for_levels(total_weight)
        lower_distribution[self._game_level] = self.quantity_main_level_creatures

        return lower_distribution

    def _get_available_levels(self):
        return list(range(0, self._game_level))

    def _calculate_weights(self):
        return [1 + int(2**((lvl - self._levels[0]) / 2)) for lvl in self._levels]

    def _calculate_quantity_creatures_for_levels(self, total_weight):
        return {lvl: self._calculate_creature_count(weight, total_weight) for lvl, weight
                in zip(self._levels, self._weights)}

    def _calculate_creature_count(self, weight, total_weight):
        return max(1, self.quantity_lower_level_creatures * weight // total_weight)
