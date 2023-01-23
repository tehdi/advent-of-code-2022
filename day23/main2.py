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

class Elf:
    def __init__(self, position):
        self.position = position
        self.previous = None

    def move_to(self, position):
        self.previous = self.position
        self.position = position

    def cancel_move(self):
        self.position = self.previous

    def __str__(self):
        return f"{self.position}"

class Around:
    def is_empty(self, position, current_positions):
        interesting = set([
            north_of(position), ne_of(position), east_of(position), se_of(position),
            south_of(position), sw_of(position), west_of(position), nw_of(position)])
        return interesting.isdisjoint(current_positions)
class North:
    def is_empty(self, position, current_positions):
        interesting = set([north_of(position), ne_of(position), nw_of(position)])
        return interesting.isdisjoint(current_positions)
    def get_move_from(self, position):
        return north_of(position)
class South:
    def is_empty(self, position, current_positions):
        interesting = set([south_of(position), se_of(position), sw_of(position)])
        return interesting.isdisjoint(current_positions)
    def get_move_from(self, position):
        return south_of(position)
class West:
    def is_empty(self, position, current_positions):
        interesting = set([west_of(position), nw_of(position), sw_of(position)])
        return interesting.isdisjoint(current_positions)
    def get_move_from(self, position):
        return west_of(position)
class East:
    def is_empty(self, position, current_positions):
        interesting = set([east_of(position), ne_of(position), se_of(position)])
        return interesting.isdisjoint(current_positions)
    def get_move_from(self, position):
        return east_of(position)

def north_of(position):
    return (position[0]-1, position[1])
def ne_of(position):
    return (position[0]-1, position[1]+1)
def east_of(position):
    return (position[0], position[1]+1)
def se_of(position):
    return (position[0]+1, position[1]+1)
def south_of(position):
    return (position[0]+1, position[1])
def sw_of(position):
    return (position[0]+1, position[1]-1)
def west_of(position):
    return (position[0], position[1]-1)
def nw_of(position):
    return (position[0]-1, position[1]-1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    elves = set()
    with open(filename) as input_file:
        for line_index,line in enumerate(input_file):
            for char_index, char in enumerate(line):
                if char == '#':
                    elves.add(Elf((line_index, char_index)))
    logging.debug(f"Found Elves {[str(elf) for elf in elves]}")

    around = Around()
    north = North()
    south = South()
    west = West()
    east = East()
    directions = [north, south, west, east]

    round_number = 0
    while True:
        round_number += 1
        moved = False
        current_positions = set([elf.position for elf in elves])
        new_positions = {}
        for elf in elves:
            position = elf.position
            if not around.is_empty(position, current_positions):
                for direction in directions:
                    if direction.is_empty(position, current_positions):
                        new_position = direction.get_move_from(position)
                        if new_position not in new_positions:
                            logging.debug(f"Elf {elf} wants to move to {new_position}")
                            elf.move_to(new_position)
                            new_positions[new_position] = elf
                            moved = True
                        elif (other_elf := new_positions[new_position]) is not None:
                            other_elf.cancel_move()
                            new_positions[new_position] = None
                            logging.debug(f"Elf {elf} wants to move to {new_position} but {other_elf} is already moving there. Cancelling both.")
                        break
        if not moved:
            logging.info(f"Nobody moved in round {round_number}.")
            logging.debug([str(elf) for elf in elves])
            break
        directions = directions[1:] + directions[:1]
