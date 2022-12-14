import logging
import time

logging.basicConfig(
    format='%(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
    filename='output.log'
)

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

def in_bounds(active_sand_position, min_x, max_x, max_y):
    logging.debug(f"{active_sand_position} {min_x} {max_x} {max_y}")
    x = active_sand_position[0]
    y = active_sand_position[1]
    if x < min_x: logging.debug("x < min")
    if x > max_x: logging.debug("x > max")
    if y > max_y: logging.debug("y > max")
    return (x >= min_x) and (x <= max_x) and (y <= max_y)

def print_cave(min_y, max_y, min_x, max_x, sand_position, cave, log):
    min_y = min(sand_origin[1], min_y)
    max_y = max(sand_origin[1], max_y)
    min_x = min(sand_origin[0], min_x)
    max_x = max(sand_origin[0], max_x)
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
    min_y = None
    max_y = 0
    for line in input_data:
        coords = line.split(' -> ')
        points = []
        for coord in coords:
            x_coord, y_coord = split_coords(coord)
            if x_coord > max_x: max_x = x_coord
            if min_x is None or x_coord < min_x: min_x = x_coord
            if y_coord > max_y: max_y = y_coord
            if min_y is None or y_coord < min_y: min_y = y_coord
            points.append((x_coord, y_coord))
        path = fill_in_path(points)
        cave.update(path)

    sand_origin = (500, 0)
    print_cave(min_y, max_y, min_x, max_x, sand_origin, cave, logging.info)
    sand = 0
    full = False
    while not full:
        active_sand_position = sand_origin
        while True:
            # time.sleep(0.5)
            print_cave(min_y, max_y, min_x, max_x, active_sand_position, cave, logging.debug)
            down = active_sand_position[0], active_sand_position[1] + 1
            down_left = active_sand_position[0] - 1, active_sand_position[1] + 1
            down_right = active_sand_position[0] + 1, active_sand_position[1] + 1
            moved = False
            if down not in cave:
                # can fall straight down
                active_sand_position = down
                moved = True
            elif down_left not in cave:
                # can fall down-left
                active_sand_position = down_left
                moved = True
            elif down_right not in cave:
                # can fall down-right
                active_sand_position = down_right
                moved = True
            
            if moved:
                if not in_bounds(active_sand_position, min_x, max_x, max_y):
                    # fell off the edge
                    print_cave(min_y, max_y, min_x, max_x, active_sand_position, cave, logging.info)
                    logging.info(f"Sand #{sand + 1} fell off the edge at {active_sand_position}")
                    full = True
                    break
            else:
                # came to rest
                sand += 1
                print_cave(min_y, max_y, min_x, max_x, active_sand_position, cave, logging.info)
                logging.info(f"Sand #{sand} came to rest at {active_sand_position}")
                cave.add(active_sand_position)
                break
    print_cave(min_y, max_y, min_x, max_x, sand_origin, cave, logging.info)
    logging.info(f"Dropped {sand} units of sand then the next one fell off the edge")
