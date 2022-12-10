from collections import deque
import logging

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # filename='out'
)

NOOP = 0
NEWLINE = '\n'
NO_SPRITE = ' '
SPRITE = '#'

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    instructions = deque()
    for line_index,line in enumerate(input_data):
        instructions.append(NOOP)
        if line.startswith('addx'):
            modifier = int(line.split(' ')[1])
            instructions.append(modifier)

    register = 1
    sprite_indices = (0, 1, 2) # register starts at 1
    output = ''
    cycle = 1
    while len(instructions) > 0:
        instruction = instructions.popleft()
        logging.debug(f"Start of cycle {cycle}: register={register}, instruction={instruction}, sprite={sprite_indices}")
        # draw first
        logging.debug(f"  Drawing pixel {(cycle-1) % 40}")
        pixel_index = (cycle-1) % 40
        if pixel_index in sprite_indices: output += SPRITE
        else: output += NO_SPRITE
        if cycle % 40 == 0: output += NEWLINE
        # then modify register
        register += instruction
        sprite_indices = (register - 1, register, register + 1)
        logging.debug(f"  End of cycle {cycle}: register={register}, sprite={sprite_indices}")
        cycle += 1
    logging.info(f"{output}")
