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
    def __init__(self, coordinates):
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

def has_landed(coordinates, cave):
    for (x, y) in coordinates:
        if y == 0: return True
        if x in cave[y-1]: return True
    return False

def land(shape, cave):
    for (x, y) in shape.coordinates:
        cave[y].add(x)

def drop_rocks(total_rocks, shape_head, direction_head, cave):
    shape_node = shape_head
    direction_node = direction_head
    rocks_landed = 0
    highest_y = 0
    jet = True
    while rocks_landed < total_rocks:
        if not jet and has_landed(shape_node.coordinates, cave):
            land(shape_node, cave)
            highest_y = max(highest_y, shape_node.highest_y())
            rocks_landed += 1
            if rocks_landed % LOG_EVERY == 0:
                logging.info(f"Tower height after {rocks_landed} rocks have landed: {highest_y + 1}")
            shape_node = shape_node.next
            shape_node.reset_position()
            shape_node.try_move(start_x_offset, highest_y + start_y_offset, min_x, max_x, cave)
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
    return highest_y

# x increases to the right, y increases up
#  ####
SHAPE_1 = ShapeNode([(0, 0), (1, 0), (2, 0), (3, 0)])
#   #
#  ###
#   #
SHAPE_2 = ShapeNode([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)])
#    #
#    #
#  ###
SHAPE_3 = ShapeNode([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])
#  #
#  #
#  #
#  #
SHAPE_4 = ShapeNode([(0, 0), (0, 1), (0, 2), (0, 3)])
#  ##
#  ##
SHAPE_5 = ShapeNode([(0, 0), (1, 0), (0, 1), (1, 1)])

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
    start_y_offset = 4

    rocks = args.rocks
    cave = defaultdict(set)  # y: set(x, x, x, ...)
    shape_head = SHAPE_1
    shape_head.try_move(start_x_offset, start_y_offset, min_x, max_x, cave)
    highest_y = drop_rocks(rocks, shape_head, direction_head, cave)
    logging.info(f"Tower height after {rocks} rocks have landed: {highest_y + 1}")
