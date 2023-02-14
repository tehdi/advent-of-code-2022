import argparse
import logging
import time
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
            filename=output_file,
            filemode='w'
        )

class ShapeNode:
    def __init__(self, id, coordinates):
        self.id = id
        self.start_position = coordinates
        self.coordinates = coordinates
        self.next = None

    def reset_position(self):
        self.coordinates = self.start_position

    def try_move(self, delta_x, delta_y, min_x, max_x, cave):
        new_coordinates = []
        for (x, y) in self.coordinates:
            (new_x, new_y) = (x + delta_x, y + delta_y)
            if (new_y < 0): return
            if (new_x < min_x): return
            if (new_x > max_x): return
            if (new_x in cave[new_y]): return
            new_coordinates.append((new_x, new_y))
        self.coordinates = new_coordinates

    def can_move(self, new_y, new_x, min_x, max_x, cave):
        return (new_y > 0) and (min_x <= new_x <= max_x) and (new_x not in cave[new_y])

    def highest_y(self):
        return max([y for x,y in self.coordinates])

class DirectionNode:
    def __init__(self, direction, index):
        self.direction = direction
        self.next = None
        self.index = index

    def has_next(self):
        return self.next is not None

class State:
    def __init__(self, cave_profile, shape_id, direction_index):
        self.cave_profile = tuple(cave_profile)
        self.shape_id = shape_id
        self.direction_index = direction_index

    def __hash__(self):
        return hash((
            self.shape_id,
            self.direction_index,
            self.cave_profile
        ))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return (
            self.shape_id == other.shape_id
                and self.direction_index == other.direction_index
                and self.cave_profile == other.cave_profile
        )

    def __str__(self):
        return f"Cave profile: {self.cave_profile}, Shape: {self.shape_id}, Direction: {self.direction_index}"

def has_landed(coordinates, cave):
    for (x, y) in coordinates:
        if y == 0: return True
        if x in cave[y-1]: return True
    return False

def land(shape, cave):
    for (x, y) in shape.coordinates:
        cave[y].add(x)

def is_repeated_state(normalized_profile, shape_id, direction_index, states, height, rock_count):
    latest_state = State(normalized_profile, shape_id, direction_index)
    if latest_state in states:
        (matched_rock_count, matched_height) = states[latest_state]
        delta_rock_count = rock_count - matched_rock_count
        delta_height = height - matched_height
        logging.debug(f"Found a repeated state at rock {rock_count}: {str(latest_state)}")
        logging.debug(f"Rock count: {matched_rock_count} -> {rock_count} = {delta_rock_count}")
        logging.debug(f"Height: {matched_height} -> {height} = {delta_height}")
        return (True, delta_rock_count, delta_height)
    else:
        states[latest_state] = (rock_count, height)
        return (False, 0, 0)

def update_profile(shape_node, cave_profile):
    for x,y in shape_node.coordinates:
        if y > cave_profile[x]: cave_profile[x] = y
    baseline = min(cave_profile)
    return [(y-baseline) for y in cave_profile]

def drop_rocks(total_rocks, shape_head, direction_head, cave):
    shape_node = shape_head
    direction_node = direction_head
    rocks_landed = 0
    highest_y = 0
    jet = True
    cave_profile = [0]*7 # max y value for each x==index
    states = {}
    # draw_cave(shape_node, cave, 10)
    while rocks_landed < total_rocks:
        if not jet and has_landed(shape_node.coordinates, cave):
            land(shape_node, cave)
            highest_y = max(highest_y, shape_node.highest_y())
            normalized_profile = update_profile(shape_node, cave_profile)
            rocks_landed += 1
            if rocks_landed % LOG_EVERY == 0:
                logging.info(f"Tower height after {rocks_landed} rocks have landed: {highest_y + 1}")
                logging.info(f"Tower height after {rocks_landed} rocks have landed: {highest_y + 1}")
                logging.debug(f"Cave profile: {normalized_profile}; Shape: {shape_node.id}; Direction: {direction_node.index}")
            (repeated, rock_delta, y_delta) = is_repeated_state(normalized_profile, shape_node.id, direction_node.index, states, highest_y+1, rocks_landed)
            # logging.debug("Landed")
            # draw_cave(shape_node, cave, highest_y + 1)
            shape_node = shape_node.next
            shape_node.reset_position()
            shape_node.try_move(start_x_offset, highest_y + start_y_offset + 1, min_x, max_x, cave)
            # draw_cave(shape_node, cave, highest_y + start_y_offset + 5)
            jet = True
            continue
        x, y = 0, 0
        if jet:
            # move sideways
            x = direction_node.direction
            direction_node = direction_node.next
        else:
            # move down
            y = -1
        shape_node.try_move(x, y, min_x, max_x, cave)
        jet = not jet
        # draw_cave(shape_node, cave, highest_y + start_y_offset + 5)
    return (rocks_landed, highest_y)

def draw_cave(shape, cave, max_y):
    logging.debug(shape.coordinates)
    logging.debug('~~~~~~~')
    for y in range(max_y, max(-1, max_y-25), -1):
        line = ''
        for x in range(7):
            line += '#' if ((x, y) in shape.coordinates or x in cave[y]) else '.'
        logging.debug(line)
    logging.debug('~~~~~~~')
    logging.debug('')
    # input()

# x increases to the right, y increases up
#  ####
SHAPE_1 = ShapeNode(1, [(0, 0), (1, 0), (2, 0), (3, 0)])
#   #
#  ###
#   #
SHAPE_2 = ShapeNode(2, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)])
#    #
#    #
#  ###
SHAPE_3 = ShapeNode(3, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])
#  #
#  #
#  #
#  #
SHAPE_4 = ShapeNode(4, [(0, 0), (0, 1), (0, 2), (0, 3)])
#  ##
#  ##
SHAPE_5 = ShapeNode(5, [(0, 0), (1, 0), (0, 1), (1, 1)])

DIRECTION = { '>': 1, '<': -1 }

# Part 2. My god, it's full of zeroes...
# TOTAL_ROCKS = 1_000_000_000_000
TOTAL_ROCKS = 10_000
LOG_EVERY = 1_000

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    parser.add_argument('-r', '--rocks', type=int, default=TOTAL_ROCKS)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    direction_head = None
    direction_tail = None
    for line in input_data:
        for char_index,char in enumerate(line):
            direction = DirectionNode(DIRECTION[char], char_index)
            if direction_head is None:
                direction_head = direction
                direction_tail = direction_head
            else:
                direction_tail.next = direction
                direction_tail = direction
    direction_tail.next = direction_head

    SHAPE_1.next = SHAPE_2
    SHAPE_2.next = SHAPE_3
    SHAPE_3.next = SHAPE_4
    SHAPE_4.next = SHAPE_5
    SHAPE_5.next = SHAPE_1

    min_x = 0
    max_x = 6
    # new rocks spawn with 2 empty spaces on their left,
    # and 3 empty spaces below them (regardless of current built-up rock height)
    start_x_offset = 2
    start_y_offset = 3

    rocks = args.rocks
    cave = defaultdict(set)  # y: set(x, x, x, ...)
    shape_head = SHAPE_1
    shape_head.try_move(start_x_offset, start_y_offset, min_x, max_x, cave)
    rocks_landed, highest_y = drop_rocks(rocks, shape_head, direction_head, cave)
    logging.info(f"Tower height after {rocks_landed} rocks have landed: {highest_y + 1}")
