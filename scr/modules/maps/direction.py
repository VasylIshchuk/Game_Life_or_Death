from .position import Position


class Direction:
    NORTH = Position(0, -1)
    SOUTH = Position(0, 1)
    EAST = Position(1, 0)
    WEST = Position(-1, 0)

    DIRECTIONS = [NORTH, SOUTH, EAST, WEST]

