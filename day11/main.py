import logging
from collections import deque

logging.basicConfig(
    format='%(message)s',
    level=logging.DEBUG,
    # filename='output.log
)

class Monkey:
    def __init__(self, id, items, inspect_operation, test):
        self.id = id
        self.inspections = 0
        self.items = deque(items)
        self.inspect = inspect_operation
        self.test = test

    def pprint(self):
        return f"Monkey {self.id} has inspected {self.inspections} things and is holding items {self.items}"

if __name__ == '__main__':
    # with open('input.txt') as input_file:
    #     input_data = [line.rstrip('\n') for line in input_file]

    # for line_index,line in enumerate(input_data):
    #     for char_index,char in enumerate(line):
    #         pass

    monkey_zero = Monkey(0, [74, 73, 57, 77, 74],
        lambda item: item * 11,
        lambda item: 6 if item % 19 == 0 else 7
    )
    monkey_one = Monkey(1, [99, 77, 79],
        lambda item: item + 8,
        lambda item: 6 if item % 2 == 0 else 0
    )
    monkey_two = Monkey(2, [64, 67, 50, 96, 89, 82, 82],
        lambda item: item + 1,
        lambda item: 5 if item % 3 == 0 else 3
    )
    monkey_three = Monkey(3, [88],
        lambda item: item * 7,
        lambda item: 5 if item % 17 == 0 else 4
    )
    monkey_four = Monkey(4, [80, 66, 98, 83, 70, 63, 57, 66],
        lambda item: item + 4,
        lambda item: 0 if item % 13 == 0 else 1
    )
    monkey_five = Monkey(5, [81, 93, 90, 61, 62, 64],
        lambda item: item + 7,
        lambda item: 1 if item % 7 == 0 else 4
    )
    monkey_six = Monkey(6, [69, 97, 88, 93],
        lambda item: item * item,
        lambda item: 7 if item % 5 == 0 else 2
    )
    monkey_seven = Monkey(7, [59, 80],
        lambda item: item + 6,
        lambda item: 2 if item % 11 == 0 else 3
    )
    monkeys = [monkey_zero, monkey_one, monkey_two, monkey_three, monkey_four, monkey_five, monkey_six, monkey_seven]
    rounds = 20
    for i in range(rounds):
        logging.debug(f"Round {i}")
        for monkey in monkeys:
            logging.debug(f"Monkey {monkey.id}")
            while len(monkey.items) > 0:
                item = monkey.items.popleft()
                item = monkey.inspect(item)
                monkey.inspections += 1
                item = item // 3 # relaaaaax! it's not broken :)
                throw_to_target = monkey.test(item)
                logging.debug(f"Monkey {monkey.id} is throwing item {item} to monkey {throw_to_target}")
                monkeys[throw_to_target].items.append(item)
    active_monkeys = sorted(monkeys, key=lambda monkey: monkey.inspections, reverse=True)
    logging.debug('\n'.join([monkey.pprint() for monkey in active_monkeys]))
