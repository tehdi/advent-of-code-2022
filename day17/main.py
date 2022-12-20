import logging

class Node:
    def __init__(self, direction, is_tail_for_real=False):
        self.direction = direction
        self.next = None
        self.is_tail_for_real = is_tail_for_real

    def has_next(self):
        return self.next is not None

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

    head = None
    tail = None
    for line in input_data:
        for char in line:
            direction = None
            if char == '>':
                direction = 1
            elif char == '<':
                direction = -1
            else:
                logging.error(f"Unrecognized directional input '{char}'")
                continue

            this = Node(direction)
            if head is None:
                head = this
                tail = head
            else:
                tail.next = this
                tail = this
    tail.is_tail_for_real = True
    tail.next = head

    node = head
    while True:
        direction = node.direction
        node = node.next
        break
