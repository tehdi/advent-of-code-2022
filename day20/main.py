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

class Node:
    id = 0

    def __init__(self, value):
        self.value = value
        self.previous = None
        self.next = None
        self.moved = False
        self.id = Node.id
        Node.id += 1

    def __str__(self):
        return f"(id={self.id}) {self.value}"

class List:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
            node.next = node
            node.previous = node
        else:
            self.tail.next = node
            self.head.previous = node
            node.previous = self.tail
            node.next = self.head
            self.tail = node
        self.length += 1

    def move_node(self, node):
        logging.debug(f"Moving node {node}")
        if node.value == 0:
            logging.debug("  no movement necessary")
            node.moved = True
            return
        steps = abs(node.value) % (self.length - 1)
        logging.debug(f"  needs to move {steps} steps")
        new_previous, new_next = self.find_node(node, steps, node.value > 0)

        logging.debug(f"  new previous: {new_previous}; next: {new_next}")
        # disconnect from old position
        old_previous = node.previous
        old_next = node.next
        old_previous.next = old_next
        old_next.previous = old_previous

        # connect to new position
        new_previous.next = node
        node.previous = new_previous
        new_next.previous = node
        node.next = new_next
        node.moved = True
        logging.debug(f"  after move: {self.pretty()}")

    def find_node(self, start_node, steps_away, forward):
        node = start_node
        for i in range(steps_away):
            if forward:
                node = node.next
            else:
                node = node.previous
        if forward: return (node, node.next)
        else: return (node.previous, node)

    def pretty(self):
        if self.head is None: return 'Empty list'
        node = self.head
        pretty = [str(node)]
        for i in range(self.length - 1): # len-1 because head is already there
            node = node.next
            pretty.append(str(node))
        return pretty

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    mixed_data = List()
    all_nodes = []
    zero_node = None
    with open(filename) as input_file:
        while (line := input_file.readline().rstrip()):
            node = Node(int(line))
            all_nodes.append(node)
            mixed_data.append(node)
            if node.value == 0: zero_node = node

    logging.debug(f"Before mixing: {mixed_data.pretty()}")
    for node in all_nodes:
        mixed_data.move_node(node)
    logging.debug(f"After mixing:  {mixed_data.pretty()}")

    node_1000 = mixed_data.find_node(zero_node, 1000 % mixed_data.length, True)[0]
    node_2000 = mixed_data.find_node(node_1000, 1000 % mixed_data.length, True)[0]
    node_3000 = mixed_data.find_node(node_2000, 1000 % mixed_data.length, True)[0]
    coordinate_1000 = node_1000.value
    coordinate_2000 = node_2000.value
    coordinate_3000 = node_3000.value
    logging.info(f"Grove coordinates: {coordinate_1000}, {coordinate_2000}, {coordinate_3000}")
    logging.info(f"Coordinate sum: {coordinate_1000 + coordinate_2000 + coordinate_3000}")

# test:
#   input:  [1, 2, -3, 3, -2, 0, 4]
#   output: [1, 2, -3, 4, 0, 3, -2]
#   coordinates: 4, -3, 2
#   coordinate sum: 3
# test2 https://www.reddit.com/r/adventofcode/comments/zr29qd/2022_day_20_part_1_python_hidden_edge_case/j11bcdy/
#   input: 0 -1 -1 1
#   in-between steps:
#       0 -1 -1 1 after moving 0
#       1 -1 0 -1 after moving -1
#       0 1 -1 -1 after moving -1
#   output: -1 1 -1 0
#   coordinates: 0, 0, 0
#   sum: 0
# test3 (wraps!) https://www.reddit.com/r/adventofcode/comments/zr29qd/2022_day_20_part_1_python_hidden_edge_case/j11d86z/
#   input: 1, 2, -3, 3, -2, 0, 8
#   sum: 7
#   -> I get 7 if I use abs(value) % (length - 1)
#   -> I get 0 if I use abs(value) % length
# not test:
#    2511 - moving abs(value)
#   11807 - moving abs(value) % (length - 1), which is too low even though test3 above works. I think the problem is if it wraps multiple times?
#   12962 is too low - moving abs(value) % length
