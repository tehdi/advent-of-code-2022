if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    elves = [0]
    for line in input_data:
        if line == '':
            elves.append(0)
        else:
            elves[-1] += int(line)

    elves.sort(reverse=True)
    print(f"The most calories carried by one Elf: {elves[0]}")
    print(f"The sum of calories carried by the top 3 Elves: {sum(elves[:3])}")
