import random

from ..core.game_entity import GameEntity

MIN_SIZE = 1
MAX_SIZE = 3


def generate_size():
    return random.randint(MIN_SIZE, MAX_SIZE)


class Chest(GameEntity):
    def __init__(self, title):
        super().__init__(title)
        self.slots = [None] * generate_size()

