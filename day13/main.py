import logging
from collections import deque

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
    # filename='output.log',
    # filemode='w',  # overwrite
)

def parse_packet(line):
    return deque(eval(line))  # I give up :)
    # MIKE SAID I SHOULD USE JSON.LOADS() BUT HE'S NOT HERE, IS HE?!

def is_int(value):
    return type(value) == int

def as_list(value):
    return [value] if is_int(value) else value

def ordered(left, right, pair_id):
    logging.debug(f"Comparing pair {pair_id}: Left: {left} to Right: {right}")

    result = None
    if len(left) == len(right) == 0:
        logging.debug("both empty is neutral")
    elif len(left) == 0 and len(right) > 0:
        logging.debug("empty left is good")
        result = True
    elif len(left) > 0 and len(right) == 0:
        logging.debug("empty right is bad")
        result = False
    else:
        left_value = left.popleft()
        right_value = right.popleft()
        logging.debug(f"Popped values: {left_value}    {right_value}")

        if is_int(left_value) and is_int(right_value):
            logging.debug(f"both ints {left_value} {right_value}")
            if left_value > right_value:
                result = False
            elif left_value < right_value:
                result = True
            else:
                result = ordered(left, right, f"{pair_id}>")
        elif is_int(left_value) or is_int(right_value):
            logging.debug("type mismatch")
            left.appendleft(as_list(left_value))
            right.appendleft(as_list(right_value))
            result = ordered(left, right, f"{pair_id}>")
        else:
            if left_value == right_value:
                logging.debug("equal lists is neutral")
                result = ordered(left, right, f"{pair_id}>")
            else:
                logging.debug("unequal lists")
                left_value = deque(left_value)
                right_value = deque(right_value)
                while result is None and len(left_value) > 0:
                    logging.debug("in while")
                    result = ordered(left_value, right_value, f"{pair_id}>")
                logging.debug(f"out of while. result={result}, leftvalue={len(left_value)}")

    logging.debug(f"Pair {pair_id} result: {result}")
    return True if result is None else result

if __name__ == '__main__':
    # with open('customtest_input.txt') as input_file:
    # with open('test_input.txt') as input_file:
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file if line != '\n']

    pairs = deque(input_data)
    pair_index = 1
    ordered_pairs = []
    while len(pairs) > 0:
        left = parse_packet(pairs.popleft())
        right = parse_packet(pairs.popleft())
        if ordered(left, right, pair_index): ordered_pairs.append(pair_index)
        pair_index += 1

    # expected_test_ordered_pairs = [1, 2, 4, 6]
    # logging.debug(f"Expected test result: {len(expected_test_ordered_pairs)} with a sum of {sum(expected_test_ordered_pairs)}: {expected_test_ordered_pairs}")
    logging.info(f"Of {len(input_data) // 2} packet pairs, {len(ordered_pairs)} are in the right order for a sum of {sum(ordered_pairs)}: {ordered_pairs}")
