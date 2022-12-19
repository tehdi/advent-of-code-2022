import logging

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
    # filename='output.log'
)

TEST = 'test'
CUSTOM = 'custom'
REAL = 'real'

if __name__ == '__main__':
    mode = TEST

    filename = 'test_input.txt'
    if mode == REAL:
        filename = 'input.txt'
    elif mode == CUSTOM:
        filename = 'customtest_input.txt'

    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    # for line_index,line in enumerate(input_data):
    for line in input_data:
        # for char_index,char in enumerate(line):
        for char in line:
            pass
