STATS = {
    "Companions": {
        "health_points": (15, 25),
        "defense": (0, 5),
        "agility": (0, 2),
    },
    "WeakEnemies": {
        "health_points": (10, 20),
        "defense": (0, 0),
        "agility": (0, 2),
    },
    "BasicEnemies": {
        "health_points": (20, 30),
        "defense": (0, 5),
        "agility": (3, 6),
    },
    "NormalEnemies": {
        "health_points": (30, 40),
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
        return STATS.get(category, None)
