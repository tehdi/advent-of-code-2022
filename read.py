import logging

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
    # filename='output.log'
)

if __name__ == '__main__':
    with open('test_input.txt') as input_file:
    # with open('customtest_input.txt') as input_file:
    # with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    # for line_index,line in enumerate(input_data):
    for line in input_data:
        # for char_index,char in enumerate(line):
        for char in line:
            pass
