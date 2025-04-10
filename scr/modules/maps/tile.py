from ..core.icons import Icon


class Tile:
    BARRIER = (Icon.WALL, Icon.GRATE, Icon.CLOSED_LEVEL_EXIT)
    CONDITIONAL = (Icon.GATEWAY_ENTRANCE, Icon.STAIRS)

    STATE_CONDITIONAL = 'CONDITIONAL'
    STATE_IMPASSABLE = 'IMPASSABLE'
    STATE_PASSABLE = 'PASSABLE'

    def __init__(self, icon):
        self.icon = icon
        self.state = self._is_passable()

    def _is_passable(self):
        if self.icon in self.CONDITIONAL:
            return self.STATE_CONDITIONAL
        elif self.icon in self.BARRIER:
            return self.STATE_IMPASSABLE
        else:
            return self.STATE_PASSABLE
