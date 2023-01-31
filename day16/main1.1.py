import argparse
import logging
import re
from random import choice

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

SINGLE_PATH_DISTANCE = 1
VALVE_ACTIVATION_TIME = 1
STARTING_TIME = 30

class Valve:
    def __init__(self, name, flow_rate, adjacent_valve_names):
        self.name = name
        self.flow_rate = flow_rate
        self.adjacent_valve_names = adjacent_valve_names
        self.adjacent_valves = []
        self.open = False

    def open(self):
        self.open = True
        return self.flow_rate

    def update_adjacent(self, valves):
        for valve in valves:
            if valve.name in self.adjacent_valve_names:
                self.adjacent_valves.append(valve)

    def __str__(self):
        status = 'OPEN' if self.open else 'CLOSED'
        return f"Valve {self.name} with flow rate {self.flow_rate} is {status}. Adjacent valves: {self.adjacent_valves}"

def next_closest(unvisited_valves, distance_to):
    closest_valve = None
    closest_valve_distance = None
    for valve in unvisited_valves:
        if closest_valve is None or closest_valve_distance is None:
            closest_valve = valve
            closest_valve_distance = distance_to[valve.name]
        else:
            distance = distance_to[valve.name]
            if distance is not None and distance < closest_valve_distance:
                closest_valve = valve
                closest_valve_distance = distance
    return closest_valve, closest_valve_distance

def plot_path_between(source, destination, valves):
    unvisited_valves = set() # valve
    distance_to = {} # valve_name: distance
    previous = {} # valve_name: previous valve along shortest path to this valve
    for valve in valves:
        unvisited_valves.add(valve)
        distance_to[valve.name] = None
        previous[valve.name] = None
    distance_to[source.name] = 0
    while len(unvisited_valves) > 0:
        current_valve, distance_to_current = next_closest(unvisited_valves, distance_to)
        if current_valve.name == destination.name:
            previous_valve = current_valve
            backtrack = [previous_valve]
            while previous_valve.name is not source.name:
                previous_valve = previous[previous_valve.name]
                backtrack.append(previous_valve)
            return backtrack[::-1]
        unvisited_valves.remove(current_valve)
        for adjacent in current_valve.adjacent_valves:
            if adjacent not in unvisited_valves: continue
            distance_from_current_to_adjacent = distance_to_current + SINGLE_PATH_DISTANCE
            previous_distance_to_adjacent = distance_to[adjacent.name]
            if previous_distance_to_adjacent is None or previous_distance_to_adjacent > distance_from_current_to_adjacent:
                distance_to[adjacent.name] = distance_from_current_to_adjacent
                previous[adjacent.name] = current_valve

def choose_next_target(targets, paths_from_current, time_remaining):
    return choice(targets)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    valves = []
    line_pattern = re.compile("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
    for line in input_data:
        m = line_pattern.match(line)
        valve_name = m.group(1)
        flow_rate = int(m.group(2))
        adjacent_valve_names = m.group(3).split(', ')
        valve = Valve(valve_name, flow_rate, adjacent_valve_names)
        valves.append(valve)
    for valve in valves:
        valve.update_adjacent(valves)

    # pre-calculate paths between valves
    paths = {} # valve_name: { other_valve_name: [path] }
    for valve in valves:
        paths[valve.name] = {} # other_valve_name: [path]
        for other_valve in valves:
            if valve.name == other_valve.name: continue
            if other_valve.flow_rate == 0: continue
            path = plot_path_between(valve, other_valve, valves)
            paths[valve.name][other_valve.name] = path

    time_remaining = STARTING_TIME
    current_position = 'AA'
    opened_valves = []
    flow_rate = 0
    total_flow = 0
    target_valves = [valve for valve in valves if valve.flow_rate > 0]
    while time_remaining > 0:
        valid_targets = [target for target in target_valves if len(paths[current_position][target.name]) <= time_remaining]
        if len(valid_targets) > 0:
            logging.debug(f"At {current_position}")
            # pick the next valve to open
            target = choose_next_target(valid_targets, paths[current_position], time_remaining)
            activation_time = len(paths[current_position][target.name])
            total_flow += flow_rate * activation_time
            time_remaining -= activation_time
            flow_rate += target.flow_rate
            target.open = True
            opened_valves.append(target.name)
            target_valves.remove(target)
            current_position = target.name
        else:
            logging.debug(f"No time left to do anything else")
            # just hanging out until we run out of time
            total_flow += flow_rate * time_remaining
            time_remaining = 0
    logging.info(f"Opened valves {opened_valves} for a total flow of {total_flow}")
