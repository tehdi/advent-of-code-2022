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

def apply(first_value, operator, second_value):
    if operator == '+': return first_value + second_value
    if operator == '-': return first_value - second_value
    if operator == '*': return first_value * second_value
    if operator == '/': return first_value / second_value
    raise Exception(f"Unknown operator '{operator}'")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    monkeys = {}
    with open(filename) as input_file:
        while (line := input_file.readline().rstrip()):
            name,value = line.split(': ')
            monkeys[name] = value

    operations = {}
    while len(operations) < len(monkeys):
        for name,value in monkeys.items():
            if name in operations: continue
            if ' ' in value:
                first_value, operator, second_value = value.split(' ')
                if first_value in operations and second_value in operations:
                    operations[name] = apply(operations[first_value], operator, operations[second_value])
            else:
                operations[name] = int(value)
    logging.debug(operations)
    logging.info(f"Root is going to yell {operations['root']}")
