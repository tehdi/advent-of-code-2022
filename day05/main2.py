from collections import defaultdict
import re

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    stacks = defaultdict(list)

    initial_setup = True
    for line in input_data:
        if initial_setup and line == '': initial_setup = False
        if initial_setup:
            for char_index,char in enumerate(line):
                if char.isalpha():
                    # 1 = 1, 5 = 2, 13 = 4, 21 = 6, ...
                    stacks[(char_index + 3) / 4].insert(0, char)
        elif line != '':
            instructions = re.search(r"move (\d+) from (\d+) to (\d+)", line)
            count, source, destination = int(instructions.group(1)), int(instructions.group(2)), int(instructions.group(3))
            # print(f"Moving {count} crates from stack {source} to stack {destination}")
            stacks[destination].extend(stacks[source][-count:])
            stacks[source] = stacks[source][:-count]

print(stacks)
tops = ''
for i in range(len(stacks)):
    top = stacks[i+1].pop()
    tops += top
    print(f"Stack {i+1}: {top}")
print(tops)
