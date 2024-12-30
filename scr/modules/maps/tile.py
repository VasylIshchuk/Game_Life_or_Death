from ..core.colors import Color


class Tile:
    ENTRANCE = f"{Color.DARK_SPRING_GREEN_BACKGROUND}{Color.DARK_SPRING_GREEN_TEXT}   {Color.RESET}"
    EXIT = f"{Color.DARK_SPRING_GREEN_BACKGROUND}{Color.DARK_SPRING_GREEN_TEXT} * {Color.RESET}"

    ROOM_FLOOR = f"{Color.BLOOD_RED_BACKGROUND}{Color.WHITE_TEXT} · {Color.RESET}"
    CORRIDOR_FLOOR = f"{Color.DARK_VANILLA_BACKGROUND}{Color.BLOOD_RED_TEXT} · {Color.RESET}"
    DOOR = f"{Color.NATURAL_WOOD_BROWN_BACKGROUND}{Color.NATURAL_WOOD_BROWN_TEXT} * {Color.RESET}"
    WALL = '   '

    BARRIER = (WALL, ENTRANCE)
    CONDITIONAL = (DOOR, EXIT)

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
