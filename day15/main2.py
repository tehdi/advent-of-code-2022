import logging
import re
from collections import defaultdict

logging.basicConfig(
    format='%(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
    # filename='output.log'
)

def extract_locations(line_pattern, line):
    m = line_pattern.match(line)
    sensor = (int(m.group(1)), int(m.group(2)))
    beacon = (int(m.group(3)), int(m.group(4)))
    return (sensor, beacon)

def calculate_radius(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1]) + 1

def find_perimeter_points(midpoint, radius, coord_max):
    points = set()
    for y_offset in range(radius + 1):
        radius_here = radius - y_offset
        x1 = midpoint[0] - radius_here
        x2 = midpoint[0] + radius_here
        y1 = midpoint[1] - y_offset
        y2 = midpoint[1] + y_offset

        usable_xs = []
        usable_ys = []
        if 0 <= x1 <= coord_max: usable_xs.append(x1)
        if 0 <= x2 <= coord_max: usable_xs.append(x2)
        if 0 <= y1 <= coord_max: usable_ys.append(y1)
        if 0 <= y2 <= coord_max: usable_ys.append(y2)
        for x in usable_xs:
            for y in usable_ys:
                yield (x, y)
                # points.add((x, y))
    # return points

# def find_all_points(midpoint, radius):
#     points = set()
#     for y_offset in range(radius + 1):
#         radius_here = radius - y_offset
#         for x_offset in range(radius_here):
#             points.add((midpoint[0] + x_offset, midpoint[1] + y_offset))
#             points.add((midpoint[0] + x_offset, midpoint[1] - y_offset))
#             points.add((midpoint[0] - x_offset, midpoint[1] + y_offset))
#             points.add((midpoint[0] - x_offset, midpoint[1] - y_offset))
#     return points

def can_see(midpoint, radius, target):
    return calculate_radius(midpoint, target) <= radius

TEST = 'test'
CUSTOM = 'custom'
REAL = 'real'

if __name__ == '__main__':
    mode = REAL

    filename = 'test_input.txt'
    coord_max = 20
    if mode == REAL:
        filename = 'input.txt'
        coord_max = 4_000_000
    elif mode == CUSTOM:
        filename = 'customtest_input.txt'

    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    sensors = []
    line_pattern = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    covered_area = defaultdict(set)
    for sensor_id,line in enumerate(input_data):
        sensor, beacon = extract_locations(line_pattern, line)
        radius = calculate_radius(sensor, beacon)
        sensors.append((sensor, radius))

    # diamonds = set()
    # for (sensor, radius) in sensors:
    #     logging.debug(f"Checking sensor {sensor} with radius {radius}")
    #     edges = find_all_points(sensor, radius)
    #     diamonds.update(edges)
    # logging.debug(diamonds)
    # for y in range(0, 21):
    #     line = f"{y:>2} "
    #     for x in range(0, 21):
    #         if (x, y) in diamonds:
    #             line += '#'
    #         else: line += '.'
    #     logging.debug(line)

    distress_beacon_location = None
    for (sensor, radius) in sensors:
        for adjacent_point in find_perimeter_points(sensor, radius, coord_max):
            seen = False
            for (other_sensor, other_radius) in sensors:
                logging.debug(f"Checking point {adjacent_point} from sensor at {sensor} against sensor {other_sensor} with radius {other_radius}")
                if other_sensor == sensor:
                    logging.debug("is same sensor")
                    continue
                if can_see(other_sensor, other_radius, adjacent_point):
                    logging.debug("can see")
                    seen = True
                    break
            if not seen:
                distress_beacon_location = adjacent_point
                break
        if distress_beacon_location is not None: break

    logging.info(f"No sensors can see the point at ({distress_beacon_location[0]}, {distress_beacon_location[1]})")
    logging.info(f"Tuning frequency = {(distress_beacon_location[0] * 4_000_000) + distress_beacon_location[1]}")
