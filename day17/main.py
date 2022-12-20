import logging
import time

class ShapeNode:
    def __init__(self, coordinates):
        self.start_position = coordinates
        self.coordinates = coordinates
        self.next = None

    def start_at(self, position):
        self.coordinates = self.start_position
        start_position = self.test_move(position[0], position[1])
        self.move_to(start_position)

    def test_move(self, x, y):
        new_coordinates = []
        for coordinate in self.coordinates:
            new_coordinates.append((coordinate[0] + x, coordinate[1] + y))
        return new_coordinates

    def move_to(self, new_coordinates):
        self.coordinates = new_coordinates

    def highest_y(self):
        return max([y for x,y in self.coordinates])

class DirectionNode:
    def __init__(self, direction):
        self.direction = direction
        self.next = None

    def has_next(self):
        return self.next is not None

def can_move_to(coordinates, min_x, max_x, cave):
    for (x, y) in coordinates:
        if y < 0: return False
        if x < min_x: return False
        if x > max_x: return False
        if (x, y) in cave: return False
    return True

def has_landed(coordinates, cave):
    for (x, y) in coordinates:
        if y == 0: return True
        if (x, y-1) in cave: return True
    return False

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

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
    # filename='output.log'
)

# Part 1
TOTAL_ROCKS = 2022
# Part 2. My god, it's full of zeroes...
# TOTAL_ROCKS = 1_000_000_000_000

TEST = 'test'
CUSTOM = 'custom'
REAL = 'real'

if __name__ == '__main__':
    mode = REAL

    filename = 'test_input.txt'
    if mode == REAL:
        filename = 'input.txt'
    elif mode == CUSTOM:
        filename = 'customtest_input.txt'

    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    direction_head = None
    direction_tail = None
    for line in input_data:
        for char in line:
            direction = DirectionNode(DIRECTION[char])
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
    start_position = (start_x_offset, start_y_offset - 1)

    direction_node = direction_head
    shape_node = SHAPE_1
    shape_node.start_at(start_position)
    jet = True
    cave = set()
    highest_y = 0
    rocks_landed = 0
    while rocks_landed < TOTAL_ROCKS:
        if not jet and has_landed(shape_node.coordinates, cave):
            cave.update(shape_node.coordinates)
            highest_y = max(highest_y, shape_node.highest_y())
            rocks_landed += 1
            if rocks_landed % 1000 == 0:
                logging.info(f"Tower height after {rocks_landed} rocks have landed: {highest_y + 1}")
            shape_node = shape_node.next
            shape_node.start_at((start_x_offset, highest_y + start_y_offset))
            jet = True

            # logging.debug('')
            # for y in range(10, -1, -1):
            #     line = f'{y:>2} '
            #     for x in range(7):
            #         if (x, y) in shape_node.coordinates: line += '#'
            #         elif (x, y) in cave: line += '*'
            #         else: line += '.'
            #     logging.debug(line)
            # time.sleep(0.5)
            continue

        x, y = 0, 0
        if jet:
            # move sideways
            x = direction_node.direction
            direction_node = direction_node.next
        else:
            # move down
            y = -1

        new_position = shape_node.test_move(x, y)
        if can_move_to(new_position, min_x, max_x, cave):
            shape_node.move_to(new_position)
        jet = not jet

        # logging.debug('')
        # for y in range(10, -1, -1):
        #     line = f'{y:>2} '
        #     for x in range(7):
        #         if (x, y) in shape_node.coordinates: line += '#'
        #         elif (x, y) in cave: line += '*'
        #         else: line += '.'
        #     logging.debug(line)
        # time.sleep(0.5)
    logging.info(f"Tower height after {rocks_landed} rocks have landed: {highest_y + 1}")
