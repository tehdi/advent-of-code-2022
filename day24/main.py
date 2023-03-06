import logging
import argparse
from collections import defaultdict
from collections import deque

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
            filename=output_file,
            filemode='w'
        )
WALL = '#'
GROUND = '.'
EXPEDITION = 'E'
UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'
WAIT = 'z'
BLIZZARD_CHARS = [UP, DOWN, LEFT, RIGHT]
MOVEMENT_OPTIONS = {
    UP: (-1, 0),
    DOWN: (+1, 0),
    LEFT: (0, -1),
    RIGHT: (0, +1),
    WAIT: (0, 0)
}
DIRECTIONS = {
    (-1, 0): UP,
    (+1, 0): DOWN,
    (0, -1): LEFT,
    (0, +1): RIGHT,
    (0, 0): WAIT
}

def is_blizzard(char):
    return char in BLIZZARD_CHARS

def print_valley(expedition, blizzards, walls, line_count, column_count):
    for line_index in range(line_count):
        output = ''
        for column_index in range(column_count):
            position = (line_index, column_index)
            if position == expedition: output += EXPEDITION
            elif position in walls: output += WALL
            elif position in blizzards:
                if len(blizzards[position]) == 1:
                    output += DIRECTIONS[blizzards[position][0]]
                else: output += str(len(blizzards[position]))
            else: output += GROUND
        logging.debug(output)
    logging.debug('')

def wrap_value(value, minimum, maximum):
    if value < minimum: return maximum
    if value > maximum: return minimum
    return value

def move_blizzard(position, direction, max_line_index, max_column_index):
    line = position[0] + direction[0]
    column = position[1] + direction[1]
    line = wrap_value(line, 1, max_line_index)
    column = wrap_value(column, 1, max_column_index)
    return (line, column)

def move_blizzards(blizzards, max_line_index, max_column_index):
    new_blizzards = defaultdict(list)
    for position,directions in blizzards.items():
        for direction in directions:
            new_position = move_blizzard(position, direction, max_line_index, max_column_index)
            new_blizzards[new_position].append(direction)
    return new_blizzards

def map_blizzards(minute, blizzards_by_minute, max_line_index, max_column_index):
    if minute in blizzards_by_minute: return blizzards_by_minute[minute]
    previous_minute_blizzards = map_blizzards(minute-1, blizzards_by_minute, max_line_index, max_column_index)
    blizzard = move_blizzards(previous_minute_blizzards, max_line_index, max_column_index)
    blizzards_by_minute[minute] = blizzard
    return blizzard

def in_order(minimum, middle, maximum):
    return minimum <= middle <= maximum

def can_move_to(position, blizzards, walls, start_position, destination, max_line_index, max_column_index):
    return ((position == start_position or position == destination)
        or ((1 <= position[0] <= max_line_index)
            and (1 <= position[1] <= max_column_index)
            and position not in blizzards
            and position not in walls))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    start_position = None
    destination = None
    blizzards = defaultdict(list)
    walls = []
    column_count = None
    with open(filename) as input_file:
        line_index = 0
        while (line := input_file.readline().rstrip()):
            if column_count is None: column_count = len(line)
            for char_index,char in enumerate(line):
                position = (line_index, char_index)
                if is_blizzard(char): blizzards[position].append(MOVEMENT_OPTIONS[char])
                if char == WALL: walls.append(position)
                if start_position is None and char == GROUND: start_position = position
                if char == GROUND: destination = position
            line_index += 1
    line_count = line_index
    max_line_index = line_count-2
    max_column_index = column_count-2

    blizzards_by_minute = { 0: blizzards }
    positions_by_minute = defaultdict(set)
    positions_by_minute[0].add(start_position)
    fewest_minutes = None
    path_options = deque([(0, start_position)])
    iteration = 0
    waits_queued = 0
    while (o := len(path_options)) > 0:
        (minute, position) = path_options.popleft()
        # if already found a faster route, no sense calculating anything else from here
        if fewest_minutes is not None and minute+1 > fewest_minutes: continue
        blizzards = map_blizzards(minute, blizzards_by_minute, max_line_index, max_column_index)

        if iteration % 100_000 == 0:
            logging.debug(f"{iteration}: m{minute}, p{position}, w{waits_queued:,}, o{o:,}, f{fewest_minutes}")
            #print_valley(position, blizzards, walls, line_count, column_count)
        iteration += 1

        for movement_option in MOVEMENT_OPTIONS.values():
            new_position = (position[0]+movement_option[0], position[1]+movement_option[1])
            if can_move_to(new_position, blizzards, walls, start_position, destination, max_line_index, max_column_index):
                if new_position == destination:
                    if fewest_minutes is None or minute < fewest_minutes: fewest_minutes = minute
                else:
                    if movement_option == MOVEMENT_OPTIONS[WAIT]: waits_queued += 1
                    new_minute = minute + 1
                    if new_position in positions_by_minute[new_minute]: continue
                    path_options.append((new_minute, new_position))
                    positions_by_minute[new_minute].add(new_position)

    logging.info(f"Fastest route found took {fewest_minutes} minutes")
