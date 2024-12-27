import random

from position import Position

LAST_ELEMENT = -1
NORTH = Position(0, -1)
SOUTH = Position(0, 1)
EAST = Position(1, 0)
WEST = Position(-1, 0)
DIRECTIONS = [NORTH, SOUTH, EAST, WEST]
WINDING_PROBABILITY = 0.5


def initialize_starting_position(temple, start_position):
    temple.carve(start_position.x, start_position.y)


def get_available_directions(temple, cell):
    available_directions = []
    for direction in DIRECTIONS:
        if can_carve(temple, cell, direction):
            available_directions.append(direction)
    return available_directions


def can_carve(temple, position: Position, direction):
    if is_within_bounds(temple, position, direction):
        return leads_to_wall(temple, position, direction)
    return False


def is_within_bounds(temple, position: Position, direction):
    cell = get_cell(position, direction, 3)
    if (0 < cell.x < temple.map_width) and (0 < cell.y < temple.map_height):
        return True
    return False


def get_cell(position: Position, direction, step):
    x = calculate_new_coordinate(position.x, direction.x, step)
    y = calculate_new_coordinate(position.y, direction.y, step)
    return Position(x, y)


def calculate_new_coordinate(base, offset, step):
    return base + offset * step


def leads_to_wall(temple, position: Position, direction):
    cell = get_cell(position, direction, 2)
    return temple.is_wall(cell.x, cell.y)


def choose_direction(last_direction, available_directions):
    if should_continue_in_last_direction(last_direction, available_directions):
        return last_direction
    return choose_random_direction(available_directions)


def should_continue_in_last_direction( last_direction, available_directions):
    """Determines if the last direction should be used again based on the "windy" probability."""
    return (last_direction in available_directions) and (random.random() > WINDING_PROBABILITY)


def choose_random_direction(available_directions):
    return random.choice(available_directions)


def carve_and_get_next_cell(temple, current_cell, direction):
    carve_corridor_by_direction(temple, current_cell, direction, 1)
    return carve_corridor_by_direction(temple, current_cell, direction, 2)


def carve_corridor_by_direction(temple, current_cell, direction, step):
    cell = get_cell(current_cell, direction, step)
    temple.carve(cell.x, cell.y)
    return cell


class Corridor:
    @staticmethod
    def generate_corridor(temple, start_position: Position):
        pending_cells = []
        last_direction = None

        initialize_starting_position(temple, start_position)

        pending_cells.append(start_position)
        while pending_cells:
            current_cell = pending_cells[LAST_ELEMENT]
            available_directions = get_available_directions(temple, current_cell)

            if available_directions:
                direction = choose_direction(last_direction, available_directions)
                next_cell = carve_and_get_next_cell(temple, current_cell, direction)
                pending_cells.append(next_cell)
                last_direction = direction
            else:
                pending_cells.pop()
                last_direction = None
