import logging
from collections import deque
from functools import cmp_to_key

logging.basicConfig(
    format='%(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
    # filename='output.log',
    # filemode='w',  # overwrite
)

DIVIDER_PACKET_1 = [[2]]
DIVIDER_PACKET_2 = [[6]]

def parse_packet(line):
    return eval(line)  # I give up :)
    # MIKE SAID I SHOULD USE JSON.LOADS() BUT HE'S NOT HERE, IS HE?!

def is_int(value):
    return type(value) == int

def as_list(value):
    return [value] if is_int(value) else value

def ordered(one, two):
    logging.debug(f"Comparing Left: {one} to Right: {two}")

    left = deque(one)
    right = deque(two)
    result = 0
    if len(left) == len(right) == 0:
        logging.debug("both empty is neutral")
    elif len(left) == 0 and len(right) > 0:
        logging.debug("empty left is good")
        result = -1
    elif len(left) > 0 and len(right) == 0:
        logging.debug("empty right is bad")
        result = 1
    else:
        left_value = left.popleft()
        right_value = right.popleft()
        logging.debug(f"Popped values: {left_value}    {right_value}")

        if is_int(left_value) and is_int(right_value):
            logging.debug(f"both ints {left_value} {right_value}")
            if left_value > right_value:
                result = 1
            elif left_value < right_value:
                result = -1
            else:
                result = ordered(left, right)
        elif is_int(left_value) or is_int(right_value):
            logging.debug("type mismatch")
            left.appendleft(as_list(left_value))
            right.appendleft(as_list(right_value))
            result = ordered(left, right)
        else:
            if left_value == right_value:
                logging.debug("equal lists is neutral")
                result = ordered(left, right)
            else:
                logging.debug("unequal lists")
                result = ordered(left_value, right_value)

    logging.debug(f"Result: {result}")
    return result

if __name__ == '__main__':
    # with open('customtest_input.txt') as input_file:
    # with open('test_input.txt') as input_file:
    with open('input.txt') as input_file:
        input_data = [parse_packet(line.rstrip('\n')) for line in input_file if line != '\n']

    input_data.append(DIVIDER_PACKET_1)
    input_data.append(DIVIDER_PACKET_2)
    ordered_pairs = sorted(input_data, key=cmp_to_key(ordered))

    logging.debug(ordered_pairs)
    # expected_test_ordered_pairs = [[], [[]], [[[]]], [1,1,3,1,1], [1,1,5,1,1], [[1],[2,3,4]], [1,[2,[3,[4,[5,6,0]]]],8,9], [1,[2,[3,[4,[5,6,7]]]],8,9], [[1],4], [[2]], [3], [[4,4],4,4], [[4,4],4,4,4], [[6]], [7,7,7], [7,7,7,7], [[8,7,6]], [9]]
    # logging.debug(f"Test data ordered as expected? {ordered_pairs == expected_test_ordered_pairs}")
    decoder_key = (ordered_pairs.index(DIVIDER_PACKET_1) + 1) * (ordered_pairs.index(DIVIDER_PACKET_2) + 1)
    logging.info(f"Decoder key: {decoder_key}")
