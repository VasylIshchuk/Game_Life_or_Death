from .position import Position


def get_position_toward_direction(position, direction):
    x = position.get_x() + direction.get_x()
    y = position.get_y() + direction.get_y()
    return Position(x, y)


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
