import logging

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
    # filename='output.log
)

def next_min_distance(distances, unvisited):
    # return key for entry with smallest value
    return sorted([location for location in distances.keys() if location in unvisited and distances[location] is not None], key=distances.get)[0]

def unvisited_neighbours_of(current, unvisited):
    potential_neighbours = [
        (current[0], current[1] - 1),
        (current[0], current[1] + 1),
        (current[0] - 1, current[1]),
        (current[0] + 1, current[1])
    ]
    return [neighbour for neighbour in potential_neighbours if neighbour in unvisited]

def can_move_between(origin, destination, local_grid):
    origin_elevation = local_grid[origin]
    destination_elevation = local_grid[destination]
    return destination_elevation + 1 >= origin_elevation

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    local_grid = {}
    start = None
    for line_index,line in enumerate(input_data):
        for char_index,char in enumerate(line):
            if char == 'E':
                start = (char_index, line_index)
                local_grid[start] = ord('z')
            else:
                local_grid[(char_index, line_index)] = ord(char)

    unvisited = set()
    distances = {}
    for location in local_grid:
        distances[location] = None
        unvisited.add(location)
    distances[start] = 0

    while len(unvisited) > 0:
        current = next_min_distance(distances, unvisited)
        logging.debug(f"Next hop: {current} with distance {distances[current]}")
        if local_grid[current] == ord('a'):
            logging.info(f"Reached target at {current} in {distances[current]} steps")
            break
        unvisited.remove(current)
        for neighbour in unvisited_neighbours_of(current, unvisited):
            if can_move_between(current, neighbour, local_grid):
                if distances[neighbour] is None:
                    distances[neighbour] = distances[current] + 1
                else:
                    shortest_distance_to_neighbour = min(distances[neighbour], distances[current] + 1)
                    distances[neighbour] = shortest_distance_to_neighbour
                logging.debug(f"Neighbour {neighbour} is reachable from {current} with shortest distance {distances[neighbour]}")
            else: logging.debug(f"Neighbour {neighbour} is not reachable from {current}")
