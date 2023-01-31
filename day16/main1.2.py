import argparse
import logging
import re
import itertools

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

def plot_all_paths(valves):
    paths = {} # valve_name: { other_valve_name: [path] }
    for valve in valves:
        paths[valve.name] = {} # other_valve_name: [path]
        for other_valve in valves:
            if valve.name == other_valve.name: continue
            if other_valve.flow_rate == 0: continue
            path = plot_path_between(valve, other_valve, valves)
            paths[valve.name][other_valve.name] = path
    return paths

def calculate_path_permutations(valves):
    target_valves = sorted([valve for valve in valves if valve.flow_rate > 0], key=lambda valve: valve.name)
    return itertools.permutations(target_valves)

def is_already_calculated(sequence, calculated_sequences):
    if len(calculated_sequences) == 0: return False
    first_valve_name = sequence[0].name
    # these are sorted, so if it's gonna match anything, it's gonna be the latest
    latest_calculated_sequence = calculated_sequences[-1]
    # avoid building a new list if the first element won't match anyway
    first_match = first_valve_name == latest_calculated_sequence[0]
    return first_match and [valve.name for valve in sequence[:len(latest_calculated_sequence)]] == latest_calculated_sequence

def try_everything(permutations, paths):
    sequences_attempted = 0
    sequences_aborted = 0
    unreachable_sequences = []
    best_flow = 0
    best_sequence = None
    best_valves = None
    for sequence in permutations:
        if is_already_calculated(sequence, unreachable_sequences):
            continue

        sequences_attempted += 1
        time_remaining = STARTING_TIME
        current_position = 'AA'
        opened_valves = []
        current_flow_rate = 0
        total_flow = 0
        for target in sequence:
            activation_time = len(paths[current_position][target.name])
            if activation_time >= time_remaining:
                sequences_aborted += 1
                unreachable_sequences.append(opened_valves + [target.name])
                break
            total_flow += current_flow_rate * activation_time
            current_flow_rate += target.flow_rate
            time_remaining -= activation_time
            opened_valves.append(target.name)
            current_position = target.name
        if time_remaining > 0:
            total_flow += current_flow_rate * time_remaining
        if total_flow > best_flow:
            best_flow = total_flow
            best_sequence = sequence
            best_valves = opened_valves
        if sequences_attempted % 1 == 0:
            logging.info(f"Attempted {sequences_attempted:,}, aborted {sequences_aborted:,}, and tracking {len(unreachable_sequences):,} skippable starts")
            logging.info(f"Latest attempt: {total_flow} using valves {opened_valves} from sequence {[valve.name for valve in sequence]}")
            logging.info(f"Current best: {best_flow} using valves {best_valves} from sequence {[valve.name for valve in best_sequence]}")
    return (best_flow, best_valves, best_sequence)

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
    logging.debug(f"Plotting all paths")
    paths = plot_all_paths(valves) # valve_name: { other_valve_name: [path] }

    # calculate all possible valve-opening sequences
    # this is doable without too much hassle for the test input, where there's time to open everything
    # but not for the real input, where there's not
    # (this returns a generator)
    logging.debug(f"Calculating all permutations")
    permutations = calculate_path_permutations(valves)
    logging.debug(f"Trying everything")
    (best_flow, best_valves, best_sequence) = try_everything(permutations, paths)
    logging.info(f"Best flow {best_flow} found from opening valves {best_valves} along sequence {[valve.name for valve in best_sequence]}")
