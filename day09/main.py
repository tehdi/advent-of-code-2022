horizontal_index = 0
vertical_index = 1

def same_row(head_position, tail_position):
    return head_position[vertical_index] == tail_position[vertical_index]

def same_column(head_position, tail_position):
    return head_position[horizontal_index] == tail_position[horizontal_index]

def sign(number):
    if number < 0: return -1
    else: return 1 # yes, for 0 too. it's fine

def move_head(direction, head_position):
    old_horizontal, old_vertical = head_position[horizontal_index], head_position[vertical_index]
    if direction == 'R':
        head_position[horizontal_index] += 1
    elif direction == 'L':
        head_position[horizontal_index] -= 1
    elif direction == 'U':
        head_position[vertical_index] += 1
    elif direction == 'D':
        head_position[vertical_index] -= 1
    # print(f"Head: {[old_horizontal, old_vertical]} + {direction} = {head_position}")

def move_tail(tail_position, head_position):
    old_horizontal, old_vertical = tail_position[horizontal_index], tail_position[vertical_index]
    horizontal_direction = sign(head_position[horizontal_index] - tail_position[horizontal_index])
    vertical_direction = sign(head_position[vertical_index] - tail_position[vertical_index])
    if same_row(head_position, tail_position):
        tail_position[horizontal_index] += horizontal_direction
    elif same_column(head_position, tail_position):
        tail_position[vertical_index] += vertical_direction
    else:
        tail_position[horizontal_index] += horizontal_direction
        tail_position[vertical_index] += vertical_direction
    # print(f"Tail: {[old_horizontal, old_vertical]} => {tail_position}")

def touching(head_position, tail_position):
    if head_position == tail_position: return True
    horizontal_diff = abs(head_position[horizontal_index] - tail_position[horizontal_index])
    vertical_diff = abs(head_position[vertical_index] - tail_position[vertical_index])
    # print(f"Diff: {[horizontal_diff, vertical_diff]}")
    return max(horizontal_diff, vertical_diff) <= 1

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    head_position = [0, 0]
    tail_position = [0, 0]
    tail_steps = set()
    tail_steps.add((tail_position[horizontal_index], tail_position[vertical_index]))
    for line_index,line in enumerate(input_data):
        # print(line)
        direction, distance = line.split(' ')
        for i in range(int(distance)):
            move_head(direction, head_position)
            while not touching(head_position, tail_position):
                move_tail(tail_position, head_position)
                tail_steps.add((tail_position[horizontal_index], tail_position[vertical_index]))

    print(f"Head: {head_position}, tail: {tail_position}, unique positions: {len(tail_steps)}")
