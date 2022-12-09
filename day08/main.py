def look_at_tree_rows(row_range, column_range):
    visible = set()
    for row_index in row_range:
        tallest_seen = None
        for column_index in column_range:
            location = (row_index, column_index)
            this_tree_height = trees[location]
            # print(f"At: {location}, height: {this_tree_height}, tallest: {tallest_seen}")
            if tallest_seen is None or this_tree_height > tallest_seen:
                # print(" +")
                visible.add(location)
                tallest_seen = trees[location]
    return visible

def look_at_tree_columns(column_range, row_range):
    visible = set()
    for column_index in column_range:
        tallest_seen = None
        for row_index in row_range:
            location = (row_index, column_index)
            this_tree_height = trees[location]
            # print(f"At: {location}, height: {this_tree_height}, tallest: {tallest_seen}")
            if tallest_seen is None or this_tree_height > tallest_seen:
                # print(" +")
                visible.add(location)
                tallest_seen = trees[location]
    return visible

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    trees = {}
    for row_index,row in enumerate(input_data):
        for column_index,tree in enumerate(row):
            trees[(row_index, column_index)] = tree

    visible = set()
    row_count = 99
    column_count = 99

    # --> v
    # expected = set([(0, 0), (0, 3), (1, 0), (1, 1), (2, 0), (3, 0), (3, 2), (3, 4), (4, 0), (4, 1), (4, 3)])
    visible = look_at_tree_rows(range(row_count), range(column_count))
    # print(f"After first block: {len(visible)} {visible == expected}")
    print(f"After first block: {len(visible)}")

    # <-- v
    # expected.update([(0, 4), (0, 3), (1, 4), (1, 2), (2, 4), (2, 3), (2, 1), (2, 0), (3, 4), (4, 4), (4, 3)])
    visible.update(look_at_tree_rows(range(row_count), range(column_count-1, 0-1, -1)))
    # print(f"After second block: {len(visible)} {visible == expected}")
    print(f"After second block: {len(visible)}")

    # v -->
    # expected.update([(0, 0), (2, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (4, 3), (0, 4), (3, 4)])
    visible.update(look_at_tree_columns(range(column_count), range(row_count)))
    # print(f"After third block: {len(visible)} {visible == expected}")
    print(f"After third block: {len(visible)}")

    # ^ -->
    # expected.update([(4, 0), (2, 0), (4, 1), (4, 2), (3, 2), (4, 3), (4, 4), (3, 4)])
    visible.update(look_at_tree_columns(range(column_count), range(row_count-1, 0-1, -1)))
    # print(f"After fourth block: {len(visible)} {visible == expected}")
    print(f"After fourth block: {len(visible)}")
    