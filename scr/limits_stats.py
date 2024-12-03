ENEMY_STATS = {
    "WeakEnemies": {
        "health_points": (15, 20),
        "defense": (0, 5),
        "agility": (0, 4),
    },
    "NormalEnemies": {
        "health_points": (25, 35),
        "defense": (5, 10),
        "agility": (7, 9),
    },
    "MediumEnemies": {
        "health_points": (40, 50),
        "defense": (15, 20),
        "agility": (12, 15),
    },
    "StrongEnemies": {
        "health_points": (60, 70),
        "defense": (30, 40),
        "agility": (20, 22),
    },
    "VeryStrongEnemies": {
        "health_points": (80, 90),
        "defense": (50, 60),
        "agility": (28, 30),
    },
}

class LimitsStats:
    @staticmethod
    def get_stats(category):
        return ENEMY_STATS.get(category, None)
