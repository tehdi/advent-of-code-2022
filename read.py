import logging

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # filename='output.log
)

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    for line_index,line in enumerate(input_data):
        for char_index,char in enumerate(line):
            pass
