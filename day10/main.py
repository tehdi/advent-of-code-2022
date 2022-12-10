from collections import deque
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

NOOP = 0

if __name__ == '__main__':
    with open('test_input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    register = 1
    instructions = deque()
    for line_index,line in enumerate(input_data):
        instructions.append(NOOP)
        if line.startswith('addx'):
            modifier = int(line.split(' ')[1])
            instructions.append(modifier)
    cycle = 1
    checksum_cycles = [20, 60, 100, 140, 180, 220]
    checksum_signal_strengths = []
    while len(instructions) > 0:
        instruction = instructions.popleft()
        if cycle in checksum_cycles:
            logging.info(f"Start of cycle {cycle}: register={register}")
            checksum_signal_strengths.append(cycle * register)
        logging.debug(f"Start of cycle {cycle}: register={register}, instruction={instruction}")
        register += instruction
        logging.debug(f"End of cycle {cycle}: register={register}")
        cycle += 1
    logging.info(f"Checksum signal strengths: {checksum_signal_strengths}, sum: {sum(checksum_signal_strengths)}")
