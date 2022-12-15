import logging

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
    filename='part2.1.log'
)

AIR = 'air'
CAVE = 'cave'
FLOOR_EXPANSION_DISTANCE = 2

class Node:
    def __init__(self, parent, location, value):
        self.parent = parent
        self.location = location
        self.value = value
        self.down = None
        self.down_left = None
        self.down_right = None

    def next_fall(self):
        if self.down.value != CAVE: return self.down
        if self.down_left.value != CAVE: return self.down_left
        if self.down_right.value != CAVE: return self.down_right
        return None

    def __str__(self):
        return f"{self.location}"

def split_coords(input):
    coords = input.split(',')
    x_coord = coords[0]
    y_coord = coords[1]
    return int(x_coord), int(y_coord)

def fill_in_path(points):
    starting_point = None
    paths_between = []
    for i in range(len(points) - 1):
        start = points[i]
        finish = points[i+1]
        x_start = min(start[0], finish[0])
        x_finish = max(start[0], finish[0])
        y_start = min(start[1], finish[1])
        y_finish = max(start[1], finish[1])
        for x in range(x_start, x_finish + 1):
            for y in range(y_start, y_finish + 1):
                paths_between.append((x, y))
    points.extend(paths_between)
    return points

def expand_floor(floor_y, mid_x, distance):
    logging.debug(f"Expanding floor {distance} points in either direction around x midpoint {mid_x}")
    return fill_in_path([(mid_x - distance, floor_y), (mid_x + distance, floor_y)])

def find_value(location, cave, floor_y):
    if (location[1] == floor_y) or (location in cave):
        return CAVE
    return AIR

def print_cave(min_y, max_y, min_x, max_x, sand_position, cave, log):
    min_y = min(sand_position[1], min_y)
    max_y = max(sand_position[1], max_y)
    min_x = min(sand_position[0], min_x)
    max_x = max(sand_position[0], max_x)
    log(f"{min_x} ---> {max_x}")
    for y in range(min_y, max_y + 1):
        line = f"{y:>3}  "
        for x in range(min_x, max_x + 1):
            if (x, y) == sand_position: line += '+'
            elif (x, y) in cave: line += '#'
            else: line += '.'
        log(line)

if __name__ == '__main__':
    # with open('customtest_input.txt') as input_file:
    # with open('test_input.txt') as input_file:
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    cave = set()
    min_x = None
    max_x = 0
    min_y = 0
    max_y = 0
    for line in input_data:
        coords = line.split(' -> ')
        points = []
        for coord in coords:
            x_coord, y_coord = split_coords(coord)
            if x_coord > max_x: max_x = x_coord
            if min_x is None or x_coord < min_x: min_x = x_coord
            if y_coord > max_y: max_y = y_coord
            if y_coord < min_y: min_y = y_coord
            points.append((x_coord, y_coord))
        path = fill_in_path(points)
        cave.update(path)
    max_y += 2  # == floor y
    floor_left = (min_x, max_y)
    floor_right = (max_x, max_y)
    path = fill_in_path([floor_left, floor_right])
    cave.update(path)

    logging.debug(f"{min_x} {max_x} {min_y} {max_y}")

    x_range = range(min_x, max_x + 1)
    y_range = range(min_y, max_y + 1)
    sand_origin = (500, 0)
    print_cave(min_y, max_y, min_x, max_x, sand_origin, cave, logging.info)
    origin = Node(None, sand_origin, True)
    drop_point = origin
    sand_units = 0
    while True:
        print_cave(min_y, max_y, min_x, max_x, drop_point.location, cave, logging.debug)
        if drop_point.down is None:
            down = (drop_point.location[0], drop_point.location[1] + 1)
            drop_point.down = Node(drop_point, down, find_value(down, cave, max_y))

        if drop_point.down_left is None:
            down_left = (drop_point.location[0] - 1, drop_point.location[1] + 1)
            drop_point.down_left = Node(drop_point, down_left, find_value(down_left, cave, max_y))

        if drop_point.down_right is None:
            down_right = (drop_point.location[0] + 1, drop_point.location[1] + 1)
            drop_point.down_right = Node(drop_point, down_right, find_value(down_right, cave, max_y))

        if drop_point.location[1] + 1 == max_y:
            cave.update(expand_floor(max_y, drop_point.location[0], FLOOR_EXPANSION_DISTANCE))
            min_x = min(min_x, drop_point.location[0] - FLOOR_EXPANSION_DISTANCE)
            max_x = max(max_x, drop_point.location[0] + FLOOR_EXPANSION_DISTANCE)

        next_fall = drop_point.next_fall()
        if next_fall is None:
            # this sand has nowhere to go
            sand_units += 1
            drop_point.value = CAVE
            cave.add(drop_point.location)
            if drop_point.parent is None:
                logging.info(f"{drop_point} has no next fall available and no parent to go back to")
                break
            else:
                drop_point = drop_point.parent
        else:
            drop_point = next_fall

    print_cave(min_y, max_y, min_x, max_x, sand_origin, cave, logging.info)
    logging.info(f"{sand_units} units of sand were added to the map")
