from game_entity import *


class Creature(GameEntity):
    def __init__(self, icon, title, description):
        super().__init__(icon, title, description)
