class Tile:
    FLOOR = '·'
    BARRIER = ('—', '|', '#')
    CONDITIONAL = '\\'

    def __init__(self, icon):
        self.icon = icon
        self.state = self._is_passable()

    # Check if the tile is passable
    def _is_passable(self):
        if self.icon in self.CONDITIONAL:
            return 'conditional'
        elif self.icon in self.BARRIER:
            return 'impassable'
        else:
            return 'passable'
