from collections import deque

TOTAL_SPACE = 70_000_000
FREE_SPACE_NEEDED = 30_000_000

COMMAND_PREFIX = "$ "
DIRECTORY_PREFIX = "dir "

def generate_directory_id():
    next_directory_id = 1
    while True:
        yield next_directory_id
        next_directory_id += 1
directory_id = generate_directory_id()

class Directory:
    def __init__(self, name, parent):
        self.id = next(directory_id)
        self.name = name
        self.files = {}
        self.child_directories = {}
        self.parent = parent
        self.size = 0

    def add_file(self, name, size):
        self.files[name] = size
        self.cascade_add_size(size)

    def add_child(self, directory):
        self.child_directories[directory.name] = directory

    def has_children(self):
        return len(self.child_directories) > 0

    def find_child(self, name):
        return self.child_directories[name]

    def has_parent(self):
        return self.parent is not None

    def get_parent_name(self):
        if self.has_parent():
            return self.parent.name
        return ' '

    def get_parent_id(self):
        if self.has_parent():
            return self.parent.id
        return ''

    def cascade_add_size(self, size):
        self.size += size
        if self.has_parent():
            self.parent.cascade_add_size(size)

    def print_tree(self):
        print(f"{self.get_parent_id()}: {self.get_parent_name()} > {self.id}: {self.name} = {self.size}")
        for child in self.child_directories.values():
            child.print_tree()

def foo(directory, target_size):
    valid_deletion_targets = []
    if directory.size >= target_size:
        valid_deletion_targets.append(directory)
    for child in directory.child_directories.values():
        valid_deletion_targets.extend(foo(child, target_size))
    return valid_deletion_targets

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    root_directory = Directory('/', None)
    directory_stack = deque()
    for line in input_data:
        if line.startswith(COMMAND_PREFIX):
            command = line[2:]
            if command.startswith('cd'):
                destination = line[5:]
                if destination == '/':
                    directory_stack.clear()
                    directory_stack.append(root_directory)
                elif destination == '..':
                    directory_stack.pop()
                else:
                    current_directory = directory_stack[-1]
                    directory_stack.append(current_directory.find_child(destination))
        elif line.startswith(DIRECTORY_PREFIX):
            directory_name = line[4:]
            parent_directory = directory_stack[-1]
            directory = Directory(directory_name, parent_directory)
            parent_directory.add_child(directory)
        else: # is a file
            delimiter_index = line.index(' ')
            size = int(line[:delimiter_index])
            name = line[delimiter_index + 1:]
            directory_stack[-1].add_file(name, size)

    used_space = root_directory.size
    free_space = TOTAL_SPACE - used_space
    need_to_free = FREE_SPACE_NEEDED - free_space

    print(f"Total space: {TOTAL_SPACE}")  # Total space: 70_000_000
    print(f"Used: {used_space}")  # Used: 48_008_081
    print(f"Free: {free_space}")  # Free: 21_991_919
    print(f"Needed for update: {FREE_SPACE_NEEDED}")  # Needed for update: 30_000_000
    print(f"Need to free: {need_to_free}")  # Need to free: 8_008_081
    valid_deletion_targets = foo(root_directory, need_to_free)
    for directory in sorted(valid_deletion_targets, key=lambda d: d.size):
        print(f"{directory.id} {directory.name} {directory.size}")
