class Tile:
    FLOOR = '·'
    BARRIER = ('—', '|', '#')
    CONDITIONAL = '\\'

    def __init__(self, element):
        self.element = element
        self.state = self.is_passable()

    # Check if the tile is passable
    def is_passable(self):
        if self.element in self.CONDITIONAL :
            return 'conditional'
        elif self.element  in self.BARRIER:
            return 'impassable'
        else :
            return 'passable'