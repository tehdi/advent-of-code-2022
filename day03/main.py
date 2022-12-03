PRIORITIES = list(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    total_priority = 0
    for line in input_data:
        compartment_size = int(len(line)/2)
        compartment_one = set(line[:compartment_size])
        compartment_two = set(line[compartment_size:])
        mispacked_item = [i for i in compartment_one if i in compartment_two][0]
        priority = PRIORITIES.index(mispacked_item)
        total_priority += priority
        print(f"Mispacked: {mispacked_item} = {priority:2} | Total: {total_priority:4} | Full Backpack: {line}")
