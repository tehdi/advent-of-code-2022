import logging
import time

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
    filename='part2.log'
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

def expand_floor(floor_y, mid_x):
    return fill_in_path([(mid_x - 2, floor_y), (mid_x + 2, floor_y)])

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
    with open('test_input.txt') as input_file:
    # with open('input.txt') as input_file:
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
    max_y += 2  # == floor y
    floor_left = (min_x, max_y)
    floor_right = (max_x, max_y)
    path = fill_in_path([floor_left, floor_right])
    cave.update(path)

    sand_origin = (500, 0)
    print_cave(min_y, max_y, min_x, max_x, sand_origin, cave, logging.info)
    sand = 0
    full = False
    last_penultimate_sand_position = sand_origin
    while not full:
        active_sand_position = last_penultimate_sand_position
        floor_impact = False
        while True:
            # time.sleep(0.5)
            print_cave(min_y, max_y, min_x, max_x, active_sand_position, cave, logging.debug)
            down = active_sand_position[0], active_sand_position[1] + 1
            down_left = active_sand_position[0] - 1, active_sand_position[1] + 1
            down_right = active_sand_position[0] + 1, active_sand_position[1] + 1
            moved = False
            if active_sand_position[1] + 1 == max_y:
                # about to hit the floor
                floor_impact = True
                cave.update(expand_floor(max_y, active_sand_position[0]))

            if down not in cave:
                # can fall straight down
                last_penultimate_sand_position = active_sand_position
                active_sand_position = down
                moved = True
            elif down_left not in cave:
                # can fall down-left
                last_penultimate_sand_position = active_sand_position
                active_sand_position = down_left
                moved = True
            elif down_right not in cave:
                # can fall down-right
                last_penultimate_sand_position = active_sand_position
                active_sand_position = down_right
                moved = True

            if floor_impact:
                mid_x = active_sand_position[0]
                if mid_x - 2 < min_x: min_x = mid_x - 2
                if mid_x + 2 > max_x: max_x = mid_x + 2

            if not moved and (active_sand_position == sand_origin):
                # done
                full = True
                sand += 1
                logging.debug(f"Sand #{sand} is blocking origin")
                break
            elif not moved:
                # came to rest
                # don't know how far this fell to get here, but if it was "not at all" then let's reset the starting point
                if last_penultimate_sand_position == active_sand_position:
                    last_penultimate_sand_position = sand_origin
                sand += 1
                print_cave(min_y, max_y, min_x, max_x, active_sand_position, cave, logging.info)
                logging.info(f"Sand #{sand} came to rest at {active_sand_position}")
                cave.add(active_sand_position)
                break 

    print_cave(min_y, max_y, min_x, max_x, sand_origin, cave, logging.info)
    logging.info(f"Sand #{sand} is blocking the origin")
