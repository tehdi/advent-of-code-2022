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
    def __init__(self, monkey_name, left, operator=None, right=None):
        self.monkey_name = monkey_name
        self.left = left
        self.operator = operator
        self.right = right

    def eval(self):
        if self.operator is None:
            logging.debug(f"{self.monkey_name} = {self.left}")
            return self.left
        left = self.left if type(self.left) is int else self.left.eval()
        right = self.right if type(self.right) is int else self.right.eval()
        if self.operator == '+':
            value = left + right
        elif self.operator == '-':
            value = left - right
        elif self.operator == '*':
            value = left * right
        elif self.operator == '/':
            value = left / right
        elif self.operator == '==':
            value = left == right
        else:
            raise Exception(f"Unknown operator '{self.operator}'")
        logging.debug(f"{self.monkey_name} = {value}")
        return value

    def contains_human(self):
        if self.monkey_name == 'humn': return True
        left_human = type(self.left) is not int and self.left.contains_human()
        right_human = type(self.left) is not int and self.right.contains_human()
        return left_human or right_human

    def pretty(self):
        if type(self.left) is not Node:
            return f"Monkey {self.monkey_name} is yelling: {self.left}"
        else:
            first = self.left if type(self.left) is int else self.left.monkey_name
            second = self.right if type(self.right) is int else self.right.monkey_name
            return f"Monkey {self.monkey_name} is yelling: {first} {self.operator} {second}"

def reverse_operation(operator, human, other, human_left):
    if operator == '+': return human - other
    if operator == '*': return human / other
    if human_left:
        if operator == '-': return human + other
        if operator == '/': return human * other
    else:
        if operator == '-': return other - human
        if operator == '/': return other / human

def find_human_value(target_value, head):
    logging.debug(f"Walking '{head.pretty()}' to match {target_value}")
    human = target_value
    monkey = head
    while monkey.monkey_name != 'humn':
        logging.debug(f"At '{monkey.pretty()}'")
        if monkey.left.contains_human():
            human = reverse_operation(monkey.operator, human, monkey.right.eval(), human_left=True)
            monkey = monkey.left
        elif monkey.right.contains_human():
            human = reverse_operation(monkey.operator, human, monkey.left.eval(), human_left=False)
            monkey = monkey.right
        logging.debug(human)
    return human

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
    while 'root' not in operations:
        for name,math in monkeys.items():
            if ' ' in math:
                left, operator, right = math.split(' ')
                if left in operations and right in operations:
                    operations[name] = Node(name, operations[left], operator, operations[right])
            else:
                value = int(math)
                operations[name] = Node(name, value)

    root = operations['root']
    logging.debug(root.pretty())
    logging.debug(f"Root left contains human? {root.left.contains_human()}")
    logging.debug(f"Root right contains human? {root.right.contains_human()}")
    human_value = None
    if root.left.contains_human():
        human_value = find_human_value(root.right.eval(), root.left)
    elif root.right.contains_human():
        human_value = find_human_value(root.left.eval(), root.right)
    human_value = int(human_value)
    logging.info(f"Try yelling {human_value}")

    operations = {}
    while 'root' not in operations:
        for name,math in monkeys.items():
            logging.debug(f"Adding {name}: {math}")
            if ' ' in math:
                left, operator, right = math.split(' ')
                if name == 'root': operator = '=='
                if left in operations and right in operations:
                    operations[name] = Node(name, operations[left], operator, operations[right])
            else:
                value = int(math)
                if name == 'humn': value = human_value
                operations[name] = Node(name, value)

    root = operations['root']
    logging.info(f"Root: {root.left.eval()} == {root.right.eval()} ? {root.eval()}")
