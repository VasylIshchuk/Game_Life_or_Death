from .level import Level


class LevelGenerator:
    @staticmethod
    def generate_level(level_number):
        return Level(level_number)
