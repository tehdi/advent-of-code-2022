from collections import defaultdict

def look_at_tree_rows(row_count, column_start_index, column_stop_index, column_step, visibility):
    for row_index in range(row_count):
        for column_index in range(column_start_index, column_stop_index, column_step):
            location = (row_index, column_index)
            this_tree_height = trees[location]
            viewing_distance = 0
            for next_tree_column in range(column_index + column_step, column_stop_index, column_step):
                viewing_distance += 1
                if trees[(row_index, next_tree_column)] >= this_tree_height: break
            # print(f"At: {location}, height: {this_tree_height}, viewing distance: {viewing_distance}")
            visibility[location] *= viewing_distance
    return visibility

def look_at_tree_columns(column_count, row_start_index, row_stop_index, row_step, visibility):
    for column_index in range(column_count):
        for row_index in range(row_start_index, row_stop_index, row_step):
            location = (row_index, column_index)
            this_tree_height = trees[location]
            viewing_distance = 0
            for next_tree_row in range(row_index + row_step, row_stop_index, row_step):
                viewing_distance += 1
                if trees[(next_tree_row, column_index)] >= this_tree_height: break
            # print(f"At: {location}, height: {this_tree_height}, viewing distance: {viewing_distance}")
            visibility[location] *= viewing_distance
    return visibility

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    trees = {}
    for row_index,row in enumerate(input_data):
        for column_index,tree in enumerate(row):
            trees[(row_index, column_index)] = int(tree)

    visibility = defaultdict(lambda: 1)
    row_count = 99
    column_count = 99

    # --> v
    (column_start_index, column_stop_index, column_step) = (0, column_count, 1)
    visibility = look_at_tree_rows(row_count, column_start_index, column_stop_index, column_step, visibility)
    # print(f"After first block: {visibility}")

    # <-- v
    (column_start_index, column_stop_index, column_step) = (column_count - 1, -1, -1)
    visibility = look_at_tree_rows(row_count, column_start_index, column_stop_index, column_step, visibility)
    # print(f"After second block: {visibility}")

    # v -->
    (row_start_index, row_stop_index, row_step) = (0, row_count, 1)
    visibility = look_at_tree_columns(column_count, row_start_index, row_stop_index, row_step, visibility)
    # print(f"After third block: {visibility}")

    # ^ -->
    (row_start_index, row_stop_index, row_step) = (row_count - 1, -1, -1)
    visibility = look_at_tree_columns(column_count, row_start_index, row_stop_index, row_step, visibility)
    # print(f"After fourth block: {visibility}")

    print(max(visibility.values()))
