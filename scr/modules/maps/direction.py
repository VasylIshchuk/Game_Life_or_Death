from .position import Position


class Direction:
    NORTH = Position(0, -1)
    SOUTH = Position(0, 1)
    EAST = Position(1, 0)
    WEST = Position(-1, 0)

    NORTH_EAST = Position(1, -1)
    NORTH_WEST = Position(-1, -1)
    SOUTH_EAST = Position(1, 1)
    SOUTH_WEST = Position(-1, 1)

    CARDINAL_DIRECTIONS = [NORTH, SOUTH, EAST, WEST]
    COMPASS_DIRECTIONS = [NORTH, SOUTH, EAST, WEST, NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST]
