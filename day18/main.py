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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    cubes = set()
    with open(filename) as input_file:
        while (line := input_file.readline().rstrip()):
            cube = line.split(',')
            cubes.add((int(cube[0]), int(cube[1]), int(cube[2])))
    surface_area = 0
    for cube in cubes:
        exposed_sides = 6
        possible_adjacents = calculate_adjacent_coordinates(cube)
        for possible_adjacent in possible_adjacents:
            if possible_adjacent in cubes:
                exposed_sides -= 1
        surface_area += exposed_sides
    logging.info(f"Surface area: {surface_area}")
