PRIORITIES = list(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    group_packs = []
    total_priority = 0
    for line_index,line in enumerate(input_data):
        group_packs.append(set(line))
        if line_index % 3 == 2:
            badge = [b for b in group_packs[0] if b in group_packs[1] and b in group_packs[2]][0]
            priority = PRIORITIES.index(badge)
            total_priority += priority
            print(f"Line: {line_index+1:3} | Badge: {badge} = {priority:2} | Total: {total_priority:4}")
            group_packs = []
