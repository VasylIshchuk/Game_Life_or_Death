from position import *


class GameEntity:
    def __init__(self, icon, title, description):
        self.icon = icon
        self.title = title
        self.description = description
        self.position = None

    def set_position(self, position: Position):
        self.position = position