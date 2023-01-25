import logging
import argparse
from collections import defaultdict

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

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'
BLIZZARD_CHARS = [UP, DOWN, LEFT, RIGHT]
MOVEMENT_DIRECTIONS = {
    UP: (-1, 0),
    'u': (-1, 0),
    DOWN: (+1, 0),
    'd': (+1, 0),
    LEFT: (0, -1),
    'l': (0, -1),
    RIGHT: (0, +1),
    'r': (0, +1),
    'w': (0, 0),
    'z': (0, 0)
}

class Blizzard:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def move(self, walls, max_line_index, max_column_index):
        line = self.position[0]
        column = self.position[1]
        if self.direction == UP: self.position = (line-1, column)
        elif self.direction == DOWN: self.position = (line+1, column)
        elif self.direction == LEFT: self.position = (line, column-1)
        elif self.direction == RIGHT: self.position = (line, column+1)
        self.wrap(walls, max_line_index, max_column_index)

    def wrap(self, walls, max_line_index, max_column_index):
        if self.position in walls:
            line = self.position[0]
            column = self.position[1]
            if line <= 0 and self.direction == UP:
                self.position = (max_line_index, column)
            elif line > max_line_index and self.direction == DOWN:
                self.position = (1, column)
            elif column <= 0 and self.direction == LEFT:
                self.position = (line, max_column_index)
            elif column > max_column_index and self.direction == RIGHT:
                self.position = (line, 1)

def is_wall(char):
    return char == '#'
def is_blizzard(char):
    return char in BLIZZARD_CHARS

def print_valley(expedition, blizzards, walls, lines, columns):
    for line_index in range(lines):
        output = ''
        for column_index in range(columns):
            position = (line_index, column_index)
            if position == expedition: output += 'E'
            elif position in walls: output += '#'
            elif position in blizzards:
                if len(blizzards[position]) == 1: output += blizzards[position][0].direction
                else: output += str(len(blizzards[position]))
            else: output += '.'
        logging.debug(output)
    logging.debug('')

def move_blizzards(blizzards, walls, lines, columns):
    new_blizzards = defaultdict(list)
    for blizzard_list in blizzards.values():
        for blizzard in blizzard_list:
            # logging.debug(f"Moving blizzard at {blizzard.position} in direction {blizzard.direction}")
            blizzard.move(walls, lines-2, columns-2)
            new_position = blizzard.position
            # logging.debug(f" ended up at {new_position}")
            new_blizzards[new_position].append(blizzard)
    return new_blizzards

def move_expedition(expedition):
    new_position = expedition
    valid_move = True
    exit_requested = False
    movement_direction = input('Which way do you want to move? (^u vd <l >r or x to exit) ')
    if movement_direction == 'x':
        exit_requested = True
    elif movement_direction in MOVEMENT_DIRECTIONS:
        movement = MOVEMENT_DIRECTIONS[movement_direction]
        new_position = (expedition[0] + movement[0], expedition[1] + movement[1])
        if new_position in walls:
            print('That will take you into a wall.')
            valid_move = False
        elif new_position in blizzards:
            print(f"That will take you into a blizzard! ({[blizzard.direction for blizzard in blizzards[new_position]]})")
            valid_move = False
        else:
            new_position = (expedition[0] + movement[0], expedition[1] + movement[1])
    return (new_position, valid_move, exit_requested)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    expedition = None
    blizzards = defaultdict(list)
    walls = []
    columns = None
    with open(filename) as input_file:
        line_index = 0
        while (line := input_file.readline().rstrip()):
            if columns is None: columns = len(line)
            for char_index,char in enumerate(line):
                position = (line_index, char_index)
                if expedition is None and char == '.':
                    expedition = position
                if is_wall(char):
                    walls.append(position)
                if is_blizzard(char):
                    blizzards[position].append(Blizzard(position, char))
            line_index += 1
    lines = line_index
    logging.debug('Minute 0')
    print_valley(expedition, blizzards, walls, lines, columns)

    minute = 0
    while True:
        minute += 1
        blizzards = move_blizzards(blizzards, walls, lines, columns)
        logging.debug(f"Minute {minute}")
        if expedition in blizzards:
            if len(blizzards[expedition]) == 1:
                print(f"If you don't move you'll be in a blizzard moving {blizzards[expedition][0].direction}")
            else:
                print(f"If you don't move you'll be in multiple blizzards moving {[blizzard.direction for blizzard in blizzards[expedition]]}")
        print_valley(expedition, blizzards, walls, lines, columns)
        valid_move = exit_requested = False
        while not valid_move and not exit_requested:
            (new_position, valid_move, exit_requested) = move_expedition(expedition)
        if exit_requested: break
        expedition = new_position
