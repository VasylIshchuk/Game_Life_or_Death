
WHITE_TEXT = '\033[107m'
BLACK_TEXT = '\033[30m'
WHITE_BACKGROUND = '\033[97m'
BLACK_BACKGROUND = '\033[40m'
RESET = '\033[0m'

class Tile:
    FLOOR = f"{WHITE_BACKGROUND}{WHITE_TEXT}·{RESET}"
    BARRIER = ('—', '|', '+', '#')
    CONDITIONAL = '\\'
    WALL = f"{BLACK_BACKGROUND}{BLACK_TEXT}#{RESET}"
    BORDER_HORIZONTAL = '—'
    BORDER_VERTICAL = '|'
    BORDER_ANGLE = '+'

    def __init__(self, icon ):
        self.icon = icon
        self.state = self._is_passable()

    def _is_passable(self):
        if self.icon in self.CONDITIONAL:
            return 'conditional'
        elif self.icon in self.BARRIER:
            return 'impassable'
        else:
            return 'passable'
