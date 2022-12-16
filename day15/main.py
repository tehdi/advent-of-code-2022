import logging
import re
from collections import defaultdict

logging.basicConfig(
    format='%(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
    # filename='output.log'
)

def calculate_radius(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1]) + 1

def diamond(sensor_id, midpoint, radius, y_of_interest):
    points = {}
    top = midpoint[1] + radius
    bottom = midpoint[1] - radius
    if bottom <= y_of_interest <= top:
        distance_from_midpoint = abs(midpoint[1] - y_of_interest)
        radius_at_y_of_interest = radius - distance_from_midpoint
        min_x = midpoint[0] - radius_at_y_of_interest + 1
        max_x = midpoint[0] + radius_at_y_of_interest - 1
        points[(min_x, y_of_interest)] = sensor_id
        points[(max_x, y_of_interest)] = sensor_id
    return points

def do_interesting_things(covered_area, y_of_interest):
    interesting_line = {point: values for (point, values) in covered_area.items() if point[1] == y_of_interest}
    logging.info("Line of interest:")
    logging.info(interesting_line)

def extract_locations(line_pattern, line):
    m = line_pattern.match(line)
    sensor = (int(m.group(1)), int(m.group(2)))
    beacon = (int(m.group(3)), int(m.group(4)))
    return (sensor, beacon)

TEST = 'test'
CUSTOM = 'custom'
REAL = 'real'

if __name__ == '__main__':
    mode = TEST

    y_of_interest = 10
    filename = 'test_input.txt'
    if mode == REAL:
        y_of_interest = 2_000_000
        filename = 'input.txt'
    elif mode == CUSTOM:
        y_of_interest = 0
        filename = 'customtest_input.txt'

    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    line_pattern = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    covered_area = defaultdict(set)
    for sensor_id,line in enumerate(input_data):
        sensor, beacon = extract_locations(line_pattern, line)
        radius = calculate_radius(sensor, beacon)
        effect_area = diamond(sensor_id, sensor, radius, y_of_interest)
        for point in effect_area:
            covered_area[point].add(effect_area[point])
        covered_area[sensor].add(f"S{sensor_id}")
        covered_area[beacon].add(f"B{sensor_id}")

    do_interesting_things(covered_area, y_of_interest)
