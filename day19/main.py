import logging
import argparse
import re
import math
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

MINUTES = 24
# can't build anything in the first minute because I have income but no resources
# no point building anything in the last minute
MAX_BUILDS = MINUTES - 2
ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"
ALL_RESOURCES = [ORE, CLAY, OBSIDIAN, GEODE]

class Blueprint:
    def __init__(self, blueprint_id,
            ore_robot_ore_cost, clay_robot_ore_cost,
            obsidian_robot_ore_cost, obsidian_robot_clay_cost,
            geode_robot_ore_cost, geode_robot_obsidian_cost):
        self.blueprint_id = blueprint_id
        self.ore_robot_ore_cost = ore_robot_ore_cost
        self.clay_robot_ore_cost = clay_robot_ore_cost
        self.obsidian_robot_ore_cost = obsidian_robot_ore_cost
        self.obsidian_robot_clay_cost = obsidian_robot_clay_cost
        self.geode_robot_ore_cost = geode_robot_ore_cost
        self.geode_robot_obsidian_cost = geode_robot_obsidian_cost

        self.robot_costs = {
            ORE: { ORE: ore_robot_ore_cost },
            CLAY: { ORE: clay_robot_ore_cost },
            OBSIDIAN: { ORE: obsidian_robot_ore_cost, CLAY: obsidian_robot_clay_cost },
            GEODE: { ORE: geode_robot_ore_cost, OBSIDIAN: geode_robot_obsidian_cost }
        }
        self.most_expensive = {
            # don't include orebot ore cost in max ore
            # since the only reason to build orebots is to get ore to build other bots
            ORE: max(clay_robot_ore_cost, obsidian_robot_ore_cost, geode_robot_ore_cost),
            CLAY: obsidian_robot_clay_cost,
            OBSIDIAN: geode_robot_obsidian_cost
        }

    def __str__(self):
        return (f"Blueprint {self.blueprint_id}: Each ore robot costs {self.ore_robot_ore_cost} ore. " +
            f"Each clay robot costs {self.clay_robot_ore_cost} ore. " +
            f"Each obsidian robot costs {self.obsidian_robot_ore_cost} ore and {self.obsidian_robot_clay_cost} clay. " +
            f"Each geode robot costs {self.geode_robot_ore_cost} ore and {self.geode_robot_obsidian_cost} obsidian.")

def extract_blueprint(line_pattern, line):
    m = line_pattern.match(line)
    blueprint_id = int(m.group(1))
    ore_robot_ore_cost = int(m.group(2))
    clay_robot_ore_cost = int(m.group(3))
    obsidian_robot_ore_cost = int(m.group(4))
    obsidian_robot_clay_cost = int(m.group(5))
    geode_robot_ore_cost = int(m.group(6))
    geode_robot_obsidian_cost = int(m.group(7))
    return Blueprint(blueprint_id,
            ore_robot_ore_cost, clay_robot_ore_cost,
            obsidian_robot_ore_cost, obsidian_robot_clay_cost,
            geode_robot_ore_cost, geode_robot_obsidian_cost)

def copy(dictionary):
    return {key:value for key,value in dictionary.items()}

def have_income_for(robot_cost, income):
    for resource in robot_cost:
        if income[resource] == 0: return False
    return True

def at_max_production(resource, resources, income, minutes_remaining, most_expensive):
    if resource == GEODE: return False
    return (resources[resource] + income[resource] * minutes_remaining) >= (most_expensive[resource] * minutes_remaining)

def minutes_to_afford(resource, robot_cost, resources, income):
    minutes = 0
    for needed_resource,needed_amount in robot_cost.items():
        have = resources[needed_resource]
        shortage = needed_amount - have
        minutes = max(minutes, math.ceil(shortage/income[needed_resource]))
    return minutes

def credit_income(income, resources, minutes):
    for resource,amount in income.items():
        resources[resource] += amount * minutes

def build_bot(resource, robot_cost, resources, income):
    for needed_resource,needed_amount in robot_cost.items():
        resources[needed_resource] -= needed_amount
    income[resource] += 1

def find_best_geodes(blueprint):
    start_income = { ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0 } # start with 1 orebot
    start_resources = { ORE: 0, CLAY: 0, OBSIDIAN: 0, GEODE: 0 }
    build_paths = deque()
    best_geodes = 0
    for resource in ALL_RESOURCES:
        if have_income_for(blueprint.robot_costs[resource], start_income):
            # in a minute:
            # 1: spend resources to start building a bot, if any
            # 2: collect resources from completed bots
            # 3: update income based on latest build, if any
            # => credit (wait+1)m of income, subtract bot cost, and update income
            # the important part is that I don't credit income before calculating what I can afford to build
            resources = copy(start_resources)
            income = copy(start_income)
            wait_time = minutes_to_afford(resource, blueprint.robot_costs[resource], resources, income)
            time_remaining = MINUTES - wait_time - 1
            credit_income(income, resources, wait_time+1)
            build_bot(resource, blueprint.robot_costs[resource], resources, income)
            build_paths.append((time_remaining, resources, income))
    while len(build_paths) > 0:
        logging.debug(f"{len(build_paths)} paths to follow")
        (time_remaining, resources, income) = build_paths.popleft()
        logging.debug(f"Path: {time_remaining} {resources} {income}")
        if (geodes := resources[GEODE]) > best_geodes: best_geodes = geodes
        if time_remaining < 2:
            credit_income(income, resources, time_remaining)
            if (geodes := resources[GEODE]) > best_geodes: best_geodes = geodes
        if time_remaining > 1:
            for resource in [resource for resource in ALL_RESOURCES if have_income_for(blueprint.robot_costs[resource], income)]:
                if at_max_production(resource, resources, income, time_remaining, blueprint.most_expensive): continue
                wait_time = minutes_to_afford(resource, blueprint.robot_costs[resource], resources, income)
                if wait_time + 1 > time_remaining: continue
                new_resources = copy(resources)
                new_income = copy(income)
                credit_income(income, new_resources, wait_time+1)
                build_bot(resource, blueprint.robot_costs[resource], new_resources, new_income)
                build_paths.append((time_remaining-wait_time-1, new_resources, new_income))
    return best_geodes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    blueprints = []
    line_pattern = re.compile("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. " +
            "Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
    with open(filename) as input_file:
        while (line := input_file.readline().rstrip()):
            blueprints.append(extract_blueprint(line_pattern, line))

    total_quality = 0
    for blueprint in blueprints:
        best_geodes = find_best_geodes(blueprint)
        quality_level = blueprint.blueprint_id * best_geodes
        total_quality += quality_level
        logging.info(f"Blueprint {blueprint.blueprint_id}: quality level = {quality_level}, geodes = {best_geodes}")
    logging.info(f"Total quality: {total_quality}")
