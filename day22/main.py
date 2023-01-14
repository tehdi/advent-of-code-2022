import logging
import argparse

def configure_logging(verbose, output_file):
    log_level = logging.DEBUG if verbose else logging.INFO
    if output_file is None:
        logging.basicConfig(
            format='%(message)s',
            level=log_level
        )
    else:
        logging.basicConfig(
            format='%(message)s',
            level=log_level,
            filename=output_file
        )

OUT_OF_BOUNDS = ' '
OPEN_SPACE = '.'
WALL = '#'
ME = '@'
PATH = 'o'
RIGHT = 'R'
LEFT = 'L'

VERBOSE = False

TURNS = {
    ( 0,  1): {'facing': 'right', 'value': 0, RIGHT: ( 1,  0), LEFT: (-1,  0)},
    ( 1,  0): {'facing': 'down',  'value': 1, RIGHT: ( 0, -1), LEFT: ( 0,  1)},
    ( 0, -1): {'facing': 'left',  'value': 2, RIGHT: (-1,  0), LEFT: ( 1,  0)},
    (-1,  0): {'facing': 'up',    'value': 3, RIGHT: ( 0,  1), LEFT: ( 0, -1)}
}

def print_board(board, position, all_positions, heighten_log_level=False):
    if not VERBOSE and not heighten_log_level: return
    border = '-' * (len(board[0]) + 4)
    if heighten_log_level: logging.info(border)
    else: logging.debug(border)
    for row_index in range(len(board)):
        row = '| '
        for column_index in range(len(board[row_index])):
            if (row_index, column_index) == position:
                row += ME
            elif (row_index, column_index) in all_positions:
                row += PATH
            else:
                row += board[row_index][column_index]
        if heighten_log_level: logging.info(row + ' |')
        else: logging.debug(row + ' |')
    if heighten_log_level: logging.info(border)
    else: logging.debug(border)

def get_next_position(start_position, facing, board_length, board_width):
    next_row = start_position[0] + facing[0]
    if next_row == board_length: next_row = 0
    if next_row < 0: next_row = board_length - 1
    next_column = start_position[1] + facing[1]
    if next_column == board_width: next_column = 0
    if next_column < 0: next_column = board_width - 1
    return (next_row, next_column)

def move(steps, position, facing, board, max_width, all_positions):
    for i in range(steps):
        next_position = get_next_position(position, facing, len(board), max_width)
        next_tile = board[next_position[0]][next_position[1]]
        if next_tile == OPEN_SPACE:
            position = next_position
            all_positions.append(position)
            print_board(board, position, all_positions)
        elif next_tile == WALL:
            logging.debug(f"At {position} trying to move {TURNS[facing]['facing']} but ran into a wall at {next_position}")
            print_board(board, position, all_positions)
            break
        elif next_tile == OUT_OF_BOUNDS:
            while next_tile == OUT_OF_BOUNDS:
                logging.debug(f"Approaching out of bounds at {position}")
                print_board(board, position, all_positions)
                next_position = get_next_position(next_position, facing, len(board), max_width)
                next_tile = board[next_position[0]][next_position[1]]
            if next_tile == WALL:
                logging.debug(f"At {position} trying to move {TURNS[facing]['facing']} but ran into a wall at {next_position}")
                print_board(board, position, all_positions)
                break
            if next_tile == OPEN_SPACE:
                position = next_position
                all_positions.append(position)
                print_board(board, position, all_positions)
    return position

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)
    VERBOSE = args.verbose

    filename = args.input_file
    directions = ''
    board = []
    position = None
    done_board = False
    max_width = 0
    with open(filename) as input_file:
        for line_index,line in enumerate(input_file):
            line = line.rstrip()
            if line == '':
                done_board = True
            elif done_board:
                directions = line
            else:
                board.append([])
                for char_index,char in enumerate(line):
                    board[line_index].append(char)
                    if position is None and char is OPEN_SPACE:
                        position = (line_index, char_index)
                if (l := len(board[line_index])) > max_width:
                    max_width = l
    for line in board:
        while len(line) < max_width:
            line.append(' ')

    logging.debug(f"Starting at {position} facing RIGHT")
    all_positions = [position]
    print_board(board, position, all_positions)

    facing = (0, 1) # start facing RIGHT
    steps = ''
    for char_index,char in enumerate(directions):
        if char.isnumeric():
            steps += char
            if char_index == len(directions) - 1:
                position = move(int(steps), position, facing, board, max_width, all_positions)
        else:
            new_facing = TURNS[facing][char]
            logging.debug(f"Move {steps} steps {TURNS[facing]['facing']} then turn {char} to face {TURNS[new_facing]['facing']}")
            position = move(int(steps), position, facing, board, max_width, all_positions)
            facing = new_facing
            steps = ''

    print_board(board, position, all_positions, heighten_log_level=True)
    password = (1000 * (position[0] + 1)) + (4 * (position[1] + 1)) + TURNS[facing]['value']
    logging.info(f"Ended up at {position} facing {TURNS[facing]['facing']} for a password of {password}")
