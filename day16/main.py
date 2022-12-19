import logging
import re
from random import choice

logging.basicConfig(
    format='%(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
    # filename='output.log'
)

SINGLE_PATH_DISTANCE = 1
VALVE_ACTIVATION_TIME = 1
STARTING_TIME = 30

class Valve:
    def __init__(self, name, flow_rate, adjacent_valves):
        self.name = name
        self.flow_rate = flow_rate
        self.adjacent_valves = adjacent_valves
        self.open = False

    def open(self):
        self.open = True
        return self.flow_rate

    def __str__(self):
        status = 'OPEN' if self.open else 'CLOSED'
        return f"Valve {self.name} with flow rate {self.flow_rate} is {status}. Adjacent valves: {self.adjacent_valves}"

def next_closest(unvisited_valves, distance_to):
    closest_valve_name = None
    closest_valve_distance = None
    for valve_name in unvisited_valves:
        if closest_valve_name is None or closest_valve_distance is None:
            closest_valve_name = valve_name
            closest_valve_distance = distance_to[valve_name]
        else:
            distance = distance_to[valve_name]
            if distance is not None and distance < closest_valve_distance:
                closest_valve_name = valve_name
                closest_valve_distance = distance
    return closest_valve_name, closest_valve_distance

def time_to_activate(source_name, destination_name, valves):
    unvisited_valves = set()
    distance_to = {}
    for valve_name in valves:
        distance_to[valve_name] = None
        unvisited_valves.add(valve_name)
    distance_to[source_name] = 0
    while len(unvisited_valves) > 0:
        current_valve_name, distance_to_current = next_closest(unvisited_valves, distance_to)
        if current_valve_name == destination_name:
            # logging.info(f"Starting at {source_name}, it will take {distance_to[destination_name] + VALVE_ACTIVATION_TIME} minutes to travel to and activate {destination_name}")
            return {source_name: {destination_name: distance_to[destination_name] + VALVE_ACTIVATION_TIME}}
        unvisited_valves.remove(current_valve_name)
        for adjacent in valves[current_valve_name].adjacent_valves:
            if adjacent not in unvisited_valves: continue
            distance_from_current_to_adjacent = distance_to_current + SINGLE_PATH_DISTANCE
            previous_distance_to_adjacent = distance_to[adjacent]
            if previous_distance_to_adjacent is None or previous_distance_to_adjacent > distance_from_current_to_adjacent:
                distance_to[adjacent] = distance_from_current_to_adjacent

TEST = 'test'
CUSTOM = 'custom'
REAL = 'real'

if __name__ == '__main__':
    mode = REAL

    filename = 'test_input.txt'
    if mode == REAL:
        filename = 'input.txt'
    elif mode == CUSTOM:
        filename = 'customtest_input.txt'

    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    valves = {}
    line_pattern = re.compile("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
    for line in input_data:
        m = line_pattern.match(line)
        valve_name = m.group(1)
        valve = Valve(valve_name, int(m.group(2)), m.group(3).split(', '))
        valves[valve_name] = valve
    # logging.debug([str(valve) for valve in valves.values()])

    # the Totally The Best, Definitely Gonna Work plan:
    # pre-calculate the shortest path from every node to every other node
    # then, starting at AA:
    #   pick a random open valve with >0 flow rate. move to it, open it, repeat until time runs out
    # do this a bunch of times and see what numbers I come up with

    activation_times = {}
    for valve_name in valves:
        activation_times[valve_name] = {}
        for other_valve_name in valves:
            if valve_name == other_valve_name: continue
            time = time_to_activate(valve_name, other_valve_name, valves)
            activation_times[valve_name].update(time[valve_name])
    # logging.debug(activation_times)

    best_flow = 0
    attempts_since_last_best = 0
    while True:
        time_remaining = STARTING_TIME
        current_position = 'AA'
        flow_rate = 0
        total_flow = 0
        target_valves = [valve for valve in valves if valves[valve].flow_rate > 0]
        # logging.debug(target_valves)
        while time_remaining > 0:
            valid_targets = [target for target in target_valves if activation_times[current_position][target] <= time_remaining]
            if len(valid_targets) > 0:
                # pick the next valve to open
                target = choice(valid_targets)
                activation_time = activation_times[current_position][target]
                current_position = target
                total_flow += flow_rate * activation_time
                time_remaining -= activation_time
                flow_rate += valves[target].flow_rate
                valves[target].open = True
                target_valves.remove(target)
                logging.debug(f"Opened valve {target}. Flow rate is now {flow_rate}, total flow is {total_flow}. Valves remaining: {len(target_valves)}")
            else:
                # just hanging out until we run out of time
                total_flow += flow_rate * time_remaining
                logging.debug(f"All reachable are open. Flow rate of {flow_rate} gets us to {total_flow} total in the remaining {time_remaining} minutes")
                if total_flow > best_flow:
                    logging.info(f"New best flow after {attempts_since_last_best} more runs! {total_flow}")
                    best_flow = total_flow
                    attempts_since_last_best = 0
                else:
                    attempts_since_last_best += 1
                time_remaining = 0
    logging.info(f"Reached {attempts_since_last_best} attempts without a new best. Assuming previous best flow of {best_flow} is at least close")
