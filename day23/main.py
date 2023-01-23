import logging
import argparse

def configure_logging(verbose, output_file):
    log_level = logging.DEBUG if verbose else logging.INFO
    if output_file is None:
        logging.basicConfig(
            format='%(message)s',
            level=log_level
        )
    else:
        logging.basicConfig(
            format='%(message)s',
            level=log_level,
            filename=output_file
        )

class Elf:
    def __init__(self, position):
        self.position = position
        self.proposed = None

    def propose(self, proposed):
        self.proposed = proposed

    def move(self):
        self.position = self.proposed
        self.proposed = None

    def cancel_move(self):
        self.proposed = None

    def __str__(self):
        return f"{self.position}"

class Around:
    def is_empty(self, position, current_positions):
        interesting = set([
            north_of(position), ne_of(position), east_of(position), se_of(position),
            south_of(position), sw_of(position), west_of(position), nw_of(position)])
        return interesting.isdisjoint(current_positions)
class North:
    def is_empty(self, position, current_positions):
        interesting = set([north_of(position), ne_of(position), nw_of(position)])
        return interesting.isdisjoint(current_positions)
    def get_move_from(self, position):
        return north_of(position)
class South:
    def is_empty(self, position, current_positions):
        interesting = set([south_of(position), se_of(position), sw_of(position)])
        return interesting.isdisjoint(current_positions)
    def get_move_from(self, position):
        return south_of(position)
class West:
    def is_empty(self, position, current_positions):
        interesting = set([west_of(position), nw_of(position), sw_of(position)])
        return interesting.isdisjoint(current_positions)
    def get_move_from(self, position):
        return west_of(position)
class East:
    def is_empty(self, position, current_positions):
        interesting = set([east_of(position), ne_of(position), se_of(position)])
        return interesting.isdisjoint(current_positions)
    def get_move_from(self, position):
        return east_of(position)

def north_of(position):
    return (position[0]-1, position[1])
def ne_of(position):
    return (position[0]-1, position[1]+1)
def east_of(position):
    return (position[0], position[1]+1)
def se_of(position):
    return (position[0]+1, position[1]+1)
def south_of(position):
    return (position[0]+1, position[1])
def sw_of(position):
    return (position[0]+1, position[1]-1)
def west_of(position):
    return (position[0], position[1]-1)
def nw_of(position):
    return (position[0]-1, position[1]-1)

def calculate_bounds(elves):
    min_line = None
    max_line = None
    min_column = None
    max_column = None
    for elf in elves:
        if min_line is None or elf.position[0] < min_line: min_line = elf.position[0]
        if max_line is None or elf.position[0] > max_line: max_line = elf.position[0]
        if min_column is None or elf.position[1] < min_column: min_column = elf.position[1]
        if max_column is None or elf.position[1] > max_column: max_column = elf.position[1]
    return (min_line, max_line, min_column, max_column)

def print_elves(elves, min_line, max_line, min_column, max_column):
    current_positions = set([elf.position for elf in elves])
    separator = ''
    logging.debug(separator)
    for line_index in range(min_line, max_line+1):
        line = ''
        for char_index in range(min_column, max_column+1):
            if (line_index, char_index) in current_positions:
                line += '#'
            else: line += '.'
        logging.debug(line)
    logging.debug(separator)

def rotate(directions):
    return directions[1:] + directions[:1]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    elves = set()
    with open(filename) as input_file:
        for line_index,line in enumerate(input_file):
            for char_index, char in enumerate(line):
                if char == '#':
                    elves.add(Elf((line_index, char_index)))
    logging.debug(f"Found Elves {[str(elf) for elf in elves]}")

    around = Around()
    north = North()
    south = South()
    west = West()
    east = East()
    directions = [north, south, west, east]

    (min_line, max_line, min_column, max_column) = calculate_bounds(elves)
    print_elves(elves, min_line, max_line, min_column, max_column)
    for i in range(10):
        current_positions = set([elf.position for elf in elves])
        proposals = set()
        conflicts = set()
        for elf in elves:
            position = elf.position
            if around.is_empty(position, current_positions):
                elf.propose(None)
            else:
                for direction in directions:
                    if direction.is_empty(position, current_positions):
                        elf.propose(direction.get_move_from(position))
                        break
            if elf.proposed is None:
                logging.debug(f"Elf {elf} doesn't want to move")
            elif elf.proposed in proposals:
                conflicts.add(elf.proposed)
            else:
                proposals.add(elf.proposed)
        if len(proposals) == 0:
            logging.debug(f"At round {i+1}, nobody wants to move!")
            break
        for elf in elves:
            if elf.proposed is None: continue
            if elf.proposed not in conflicts:
                logging.debug(f"Elf {elf} is moving to {elf.proposed}")
                elf.move()
            else:
                logging.debug(f"Elf {elf} has a conflict and is not moving to {elf.proposed}")
                elf.cancel_move()
        directions = rotate(directions)

        (min_line, max_line, min_column, max_column) = calculate_bounds(elves)
        print_elves(elves, min_line, max_line, min_column, max_column)

    lines_covered = max_line - min_line + 1
    columns_covered = max_column - min_column + 1
    ground_covered = lines_covered * columns_covered
    elf_count = len(elves)
    empty_ground_tiles = ground_covered - elf_count
    logging.info(f"Elves are covering a rectangle {lines_covered} x {columns_covered} = {ground_covered} tiles")
    logging.info(f"Minus the {elf_count} Elves is {empty_ground_tiles} empty ground tiles")
