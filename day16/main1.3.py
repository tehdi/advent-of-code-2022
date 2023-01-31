import argparse
import logging
import re
import itertools
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

SINGLE_PATH_DISTANCE = 1
VALVE_ACTIVATION_TIME = 1
STARTING_TIME = 30

class Valve:
    def __init__(self, name, flow_rate, adjacent_valve_names):
        self.name = name
        self.flow_rate = flow_rate
        self.adjacent_valve_names = adjacent_valve_names
        self.adjacent_valves = []

    def update_adjacent(self, valves):
        for valve in valves:
            if valve.name in self.adjacent_valve_names:
                self.adjacent_valves.append(valve)

    def __str__(self):
        return f"Valve {self.name} with flow rate {self.flow_rate}. Adjacent valves: {self.adjacent_valves}"

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

def time_to_activate(source, destination, valves):
    unvisited_valves = set() # valve
    distance_to = {} # valve_name: distance
    for valve in valves:
        unvisited_valves.add(valve)
        distance_to[valve.name] = None
    distance_to[source.name] = 0
    while len(unvisited_valves) > 0:
        current_valve, distance_to_current = next_closest(unvisited_valves, distance_to)
        if current_valve.name == destination.name:
            return distance_to[destination.name] + VALVE_ACTIVATION_TIME
        unvisited_valves.remove(current_valve)
        for adjacent in current_valve.adjacent_valves:
            if adjacent not in unvisited_valves: continue
            distance_from_current_to_adjacent = distance_to_current + SINGLE_PATH_DISTANCE
            previous_distance_to_adjacent = distance_to[adjacent.name]
            if previous_distance_to_adjacent is None or previous_distance_to_adjacent > distance_from_current_to_adjacent:
                distance_to[adjacent.name] = distance_from_current_to_adjacent

def calculate_activation_times(valves):
    times = {} # valve_name: { other_valve_name: time }
    for valve in valves:
        times[valve.name] = {} # other_valve_name: activation_time
        for other_valve in valves:
            if valve.name == other_valve.name: continue
            if other_valve.flow_rate == 0: continue
            time = time_to_activate(valve, other_valve, valves)
            times[valve.name][other_valve.name] = time
    return times

def build_options(current_position, target_valves, activation_times, time_remaining, opened_valves, current_flow):
    options = deque()
    for target in target_valves:
        if target.name == current_position.name: continue
        if target in opened_valves: continue
        activation_time = activation_times[current_position.name][target.name]
        if activation_time >= time_remaining: continue
        time_after_activation = time_remaining - activation_time
        entry = (target, time_after_activation, current_flow + (time_after_activation * target.flow_rate), frozenset(opened_valves.union([target])))
        options.append(entry)
    return options

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    valves = []
    starting_position = None
    line_pattern = re.compile("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
    for line in input_data:
        m = line_pattern.match(line)
        valve_name = m.group(1)
        flow_rate = int(m.group(2))
        adjacent_valve_names = m.group(3).split(', ')
        valve = Valve(valve_name, flow_rate, adjacent_valve_names)
        valves.append(valve)
        if valve_name == 'AA': starting_position = valve
    for valve in valves:
        valve.update_adjacent(valves)

    # pre-calculate distances between valves
    logging.debug(f"Plotting all activation times")
    activation_times = calculate_activation_times(valves) # valve_name: { other_valve_name: time }

    target_valves = [valve for valve in valves if valve.flow_rate > 0]
    logging.debug([f"{valve.name}: {valve.flow_rate}" for valve in target_valves])
    # (current valve, time remaining, total relief, set of valves opened)
    current_position = starting_position
    time_remaining = STARTING_TIME
    total_flow = 0
    opened_valves = set()
    valve_subsets = deque([(current_position, time_remaining, total_flow, opened_valves)])

    logging.debug(f"Building things")
    best_flows = {} # set(valve): flow
    while len(valve_subsets) > 0:
        (current_position, time_remaining, total_flow, opened_valves) = valve_subsets.popleft()
        # logging.debug(f"At {current_position.name} with {len(valve_subsets)} values in valve subsets, {time_remaining} time remaining, {total_flow} total flow, and opened valves: {[valve.name for valve in opened_valves]}")
        for entry in build_options(current_position, target_valves, activation_times, time_remaining, opened_valves, total_flow):
            # options entry:
            #   0: position
            #   1: time remaining after activation
            #   2: total flow
            #   3: set of opened valves
            valve_subsets.append(entry)
            flow_rate = entry[2]
            opened_valves = entry[3]
            # logging.debug(f" Processing entry for {[valve.name for valve in opened_valves]} with total flow {flow_rate} and {entry[1]} time remaining")
            if (opened_valves not in best_flows) or (flow_rate > best_flows[opened_valves]):
                best_flows[opened_valves] = flow_rate
        # logging.debug(f" End: {len(valve_subsets)} values in valve subsets")

    best_flow = 0
    best_path = None
    for opened_valves,flow_rate in best_flows.items():
        if flow_rate > best_flow:
            best_flow = flow_rate
            best_path = opened_valves
    logging.info(f"Found best flow {best_flow} by opening valves {[valve.name for valve in best_path]} in... some order. It's not important.")
