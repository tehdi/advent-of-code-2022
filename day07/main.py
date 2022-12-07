from collections import deque

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

def foo(directory):
    total_size = 0
    if directory.size <= 100000:
        print(f"{directory.id} {directory.name} {directory.size}")
        total_size += directory.size
    for child in directory.child_directories.values():
        total_size += foo(child)
    return total_size

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

    # root_directory.print_tree()
    total_size = foo(root_directory)
    print(total_size)
