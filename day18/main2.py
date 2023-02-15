import logging
import argparse
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

def calculate_adjacent_coordinates(cube):
    x = cube[0]
    y = cube[1]
    z = cube[2]
    return [
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1)
    ]

def in_range(value, minimum, maximum):
    return minimum <= value <= maximum

LAVA = "lava"
AIR = "air"
BOUNDARY = "boundary"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    filename = args.input_file
    configure_logging(args.verbose, args.output_file)

    min_x, max_x = None, None
    min_y, max_y = None, None
    min_z, max_z = None, None
    cubes = {}
    with open(filename) as input_file:
        while (line := input_file.readline().rstrip()):
            cube = line.split(',')
            x, y, z = int(cube[0]), int(cube[1]), int(cube[2])
            cubes[(x, y, z)] = LAVA
            if min_x is None or x < min_x: min_x = x
            if max_x is None or x > max_x: max_x = x
            if min_y is None or y < min_y: min_y = y
            if max_y is None or y > max_y: max_y = y
            if min_z is None or z < min_z: min_z = z
            if max_z is None or z > max_z: max_z = z

    surface_area = 0
    to_explore = deque()
    to_explore.append((min_x-1, min_y-1, min_z-1))
    while len(to_explore) > 0:
        logging.debug(f"Queued for exploration: {len(to_explore)}")
        cube = to_explore.popleft()
        adjacents = calculate_adjacent_coordinates(cube)
        cubes[cube] = AIR # sane default?
        for adjacent in adjacents:
            (x, y, z) = adjacent
            if (content := cubes.get(adjacent)) is not None:
                # This adjacent cube has already been discovered! But what is it?
                logging.debug(f"{cube} Adjacent to {content} at {adjacent}!")
                if content == LAVA:
                    cubes[cube] = BOUNDARY
                    # cube could be adjacent to multiple lava cubes
                    surface_area += 1
            elif False in [
                in_range(x, min_x-1, max_x+1),
                in_range(y, min_y-1, max_y+1),
                in_range(z, min_z-1, max_z+1)
            ]:
                # This cube is out of range. Track it but don't follow up on it.
                logging.debug(f"{cube} Out of range at {adjacent}.")
                cubes[adjacent] = AIR
            else:
                if adjacent not in to_explore:
                    logging.debug(f"{cube} Needs closer inspection at {adjacent}.")
                    to_explore.append(adjacent)

    logging.info(f"Surface area: {surface_area}")
