import logging
import re
from random import choice
from collections import deque

logging.basicConfig(
    format='%(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
    # filename='output.log'
)

SINGLE_PATH_DISTANCE = 1
VALVE_ACTIVATION_TIME = 1

class Valve:
    def __init__(self, name, flow_rate, adjacent_valves):
        self.name = name
        self.flow_rate = flow_rate
        self.adjacent_valves = adjacent_valves
        self.open = False

    def __str__(self):
        status = 'OPEN' if self.open else 'CLOSED'
        return f"Valve {self.name} with flow rate {self.flow_rate} is {status}. Adjacent valves: {self.adjacent_valves}"

class TravelAction:
    def __init__(self, valve):
        self.valve = valve

    def apply(self):
        return (self.valve.name, 0)

    def __str__(self):
        return "Travel"

class OpenAction:
    def __init__(self, valve):
        self.valve = valve

    def apply(self):
        self.valve.open = True
        return (self.valve.name, self.valve.flow_rate)

    def __str__(self):
        return f"Open {self.valve.name}"

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
    while True:
        flow_rate = 0
        total_flow = 0
        time_remaining = 26
        target_valves = [valve for valve in valves.values() if valve.flow_rate > 0]
        
        my_position = 'AA'
        my_action_queue = deque()
        # the elephant's name is now Hyffle
        hyffle_position = 'AA'
        hyffle_action_queue = deque()
        while time_remaining > 0:
            total_flow += flow_rate

            # if my action queue is empty, pick a random valve for me to target
            if len(my_action_queue) == 0:
                # logging.debug(f"My current position: {my_position}")
                # logging.debug(f"My available targets: {[valve.name for valve in target_valves]}")
                my_valid_targets = [target for target in target_valves if activation_times[my_position][target.name] <= time_remaining]
                if len(my_valid_targets) > 0:
                    valve = choice(my_valid_targets)
                    # add the appropriate no-ops and open actions to my queue
                    for i in range(activation_times[my_position][valve.name] - 1):
                        my_action_queue.append(TravelAction(valve))
                    my_action_queue.append(OpenAction(valve))
                    # remove my target from the list of available targets
                    # logging.debug(f"I am removing valve {valve.name}")
                    target_valves.remove(valve)
            # if my action queue has items, pop one and process it
            if len(my_action_queue) > 0:
                my_action = my_action_queue.popleft()
                my_position, flow_rate_modifier = my_action.apply()
                flow_rate += flow_rate_modifier

            # do that ^ for Hyffle
            if len(hyffle_action_queue) == 0:
                # logging.debug(f"Hyffle's current position: {hyffle_position}")
                # logging.debug(f"Hyffle's available targets: {[valve.name for valve in target_valves]}")
                hyffle_valid_targets = [target for target in target_valves if activation_times[hyffle_position][target.name] <= time_remaining]
                if len(hyffle_valid_targets) > 0:
                    valve = choice(hyffle_valid_targets)
                    for i in range(activation_times[hyffle_position][valve.name] - 1):
                        hyffle_action_queue.append(TravelAction(valve))
                    hyffle_action_queue.append(OpenAction(valve))
                    # logging.debug(f"Hyffle is removing valve {valve.name}")
                    target_valves.remove(valve)
            if len(hyffle_action_queue) > 0:
                hyffle_action = hyffle_action_queue.popleft()
                hyffle_position, flow_rate_modifier = hyffle_action.apply()
                flow_rate += flow_rate_modifier

            time_remaining -= 1
            # logging.debug(f"My action queue: {[str(action) for action in my_action_queue]}")
            # logging.debug(f"Hyffle's action queue: {[str(action) for action in hyffle_action_queue]}")
        if total_flow > best_flow:
            logging.info(f"New best flow! {total_flow}")
            best_flow = total_flow
