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
            filename=output_file,
            filemode='w'
        )

OUT_OF_BOUNDS = ' '
OPEN_SPACE = '.'
WALL = '#'
ME = '@'
PATH = 'o'
RIGHT = 'R'
LEFT = 'L'

CHUNK_SIZE = 50

FACING_RIGHT = (0, 1)
FACING_DOWN = (1, 0)
FACING_LEFT = (0, -1)
FACING_UP = (-1, 0)

VERBOSE = False

TURNS = {
   FACING_RIGHT : {'facing': 'right', 'value': 0, RIGHT: ( 1,  0), LEFT: (-1,  0)},
   FACING_DOWN  : {'facing': 'down',  'value': 1, RIGHT: ( 0, -1), LEFT: ( 0,  1)},
   FACING_LEFT  : {'facing': 'left',  'value': 2, RIGHT: (-1,  0), LEFT: ( 1,  0)},
   FACING_UP    : {'facing': 'up',    'value': 3, RIGHT: ( 0,  1), LEFT: ( 0, -1)}
}

WRAP_MAP = {
    # square: { facing: (destination square, destination facing, function to calculate position of next step) }
    1: { FACING_RIGHT: (2, FACING_RIGHT, lambda position: ( position[0],                  CHUNK_SIZE*2             )),
         FACING_DOWN:  (3, FACING_DOWN,  lambda position: ( CHUNK_SIZE,                   position[1]              )),
         FACING_LEFT:  (4, FACING_RIGHT, lambda position: ( CHUNK_SIZE*3-1-position[0],   0                        )),
         FACING_UP:    (6, FACING_RIGHT, lambda position: ( position[1]+CHUNK_SIZE*2,     0                        ))},
    2: { FACING_RIGHT: (5, FACING_LEFT,  lambda position: ( CHUNK_SIZE*3-1-position[0],   CHUNK_SIZE*2-1           )),
         FACING_DOWN:  (3, FACING_LEFT,  lambda position: ( position[1]-CHUNK_SIZE,       CHUNK_SIZE*2-1           )),
         FACING_LEFT:  (1, FACING_LEFT,  lambda position: ( position[0],                  CHUNK_SIZE-1             )),
         FACING_UP:    (6, FACING_UP,    lambda position: ( CHUNK_SIZE*4-1,               position[1]-CHUNK_SIZE*2 ))},
    3: { FACING_RIGHT: (2, FACING_UP,    lambda position: ( CHUNK_SIZE-1,                 position[0]+CHUNK_SIZE   )),
         FACING_DOWN:  (5, FACING_DOWN,  lambda position: ( CHUNK_SIZE*2,                 position[1]              )),
         FACING_LEFT:  (4, FACING_DOWN,  lambda position: ( CHUNK_SIZE*2,                 position[0]-CHUNK_SIZE   )),
         FACING_UP:    (1, FACING_UP,    lambda position: ( CHUNK_SIZE-1,                 position[1]              ))},
    4: { FACING_RIGHT: (5, FACING_RIGHT, lambda position: ( position[0],                  CHUNK_SIZE               )),
         FACING_DOWN:  (6, FACING_DOWN,  lambda position: ( CHUNK_SIZE*3,                 position[1]              )),
         FACING_LEFT:  (1, FACING_RIGHT, lambda position: ( CHUNK_SIZE*3-1-position[0],   CHUNK_SIZE               )),
         FACING_UP:    (3, FACING_RIGHT, lambda position: ( position[1]+CHUNK_SIZE,       CHUNK_SIZE               ))},
    5: { FACING_RIGHT: (2, FACING_LEFT,  lambda position: ( CHUNK_SIZE*3-1-position[0],   CHUNK_SIZE*3-1           )),
         FACING_DOWN:  (6, FACING_LEFT,  lambda position: ( position[1]+CHUNK_SIZE*2,     CHUNK_SIZE-1             )),
         FACING_LEFT:  (4, FACING_LEFT,  lambda position: ( position[0],                  CHUNK_SIZE-1             )),
         FACING_UP:    (3, FACING_UP,    lambda position: ( CHUNK_SIZE*2-1,               position[1]              ))},
    6: { FACING_RIGHT: (5, FACING_UP,    lambda position: ( CHUNK_SIZE*3-1,               position[0]-CHUNK_SIZE*2 )),
         FACING_DOWN:  (2, FACING_DOWN,  lambda position: ( 0,                            position[1]+CHUNK_SIZE*2 )),
         FACING_LEFT:  (1, FACING_DOWN,  lambda position: ( 0,                            position[0]-CHUNK_SIZE*2 )),
         FACING_UP:    (4, FACING_UP,    lambda position: ( CHUNK_SIZE*3-1,               position[1]              ))}
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
    next_column = start_position[1] + facing[1]
    # logging.debug(f'maybe moving from p{start_position} f{facing} to p{(next_row, next_column)}')
    if find_square((next_row, next_column)) == 0:
        return wrap(start_position, facing)
    return ((next_row, next_column), facing)

def find_square(position):
    logging.info(f'finding square for p{position}')
    line_index = position[0]
    char_index = position[1]
    if 0 <= line_index <=  CHUNK_SIZE-1             and CHUNK_SIZE <= char_index <=  CHUNK_SIZE*2-1:  return 1
    if 0 <= line_index <=  CHUNK_SIZE-1             and CHUNK_SIZE*2 <= char_index <= CHUNK_SIZE*3-1: return 2
    if CHUNK_SIZE <= line_index <=  CHUNK_SIZE*2-1  and CHUNK_SIZE <= char_index <=  CHUNK_SIZE*2-1:  return 3
    if CHUNK_SIZE*2 <= line_index <= CHUNK_SIZE*3-1 and 0 <= char_index <=  CHUNK_SIZE-1:             return 4
    if CHUNK_SIZE*2 <= line_index <= CHUNK_SIZE*3-1 and CHUNK_SIZE <= char_index <=  CHUNK_SIZE*2-1:  return 5
    if CHUNK_SIZE*3 <= line_index <= CHUNK_SIZE*4-1 and 0 <= char_index <=  CHUNK_SIZE-1:             return 6
    logging.info(f'p{position} is not in a known square')
    return 0

def wrap(position, facing):
    square = find_square(position)
    (expected_square, next_facing, next_position_function) = WRAP_MAP[square][facing]
    next_position = next_position_function(position)
    if (actual_square := find_square(next_position)) != expected_square:
        raise Exception(f'fucked up wrap: s{square} @ p{position} + f{facing} => expected s{expected_square} @ p{next_position} but got s{actual_square}')
    logging.debug(f'wrapped from p{position} f{facing} to p{next_position} f{next_facing}')
    return (next_position, next_facing)

def move(steps, position, facing, board, max_width, all_positions):
    for i in range(steps):
        (next_position, next_facing) = get_next_position(position, facing, len(board), max_width)
        next_tile = board[next_position[0]][next_position[1]]

        if next_tile == OPEN_SPACE:
            # logging.debug(f'moving to p{next_position} f{facing}')
            position = next_position
            facing = next_facing
            all_positions.append(position)
        elif next_tile == WALL:
            logging.debug(f"At {position} trying to move {TURNS[facing]['facing']} but ran into a wall at {next_position}")
            break
    print_board(board, position, all_positions)
    return (position, facing)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    parser.add_argument('-c', '--chunk-size', type=int, default=CHUNK_SIZE)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)
    VERBOSE = args.verbose
    CHUNK_SIZE = args.chunk_size

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
                break
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

    facing = FACING_RIGHT
    steps = ''
    for char_index,char in enumerate(directions):
        if char.isnumeric():
            steps += char
            if char_index == len(directions) - 1:
                logging.debug(f"Move {steps} steps {TURNS[facing]['facing']} then stop")
                (position, facing) = move(int(steps), position, facing, board, max_width, all_positions)
        else:
            logging.debug(f"Move {steps} steps {TURNS[facing]['facing']} then turn {char}")
            (position, facing) = move(int(steps), position, facing, board, max_width, all_positions)
            facing = TURNS[facing][char]
            steps = ''

    print_board(board, position, all_positions, heighten_log_level=True)
    password = (1000 * (position[0] + 1)) + (4 * (position[1] + 1)) + TURNS[facing]['value']
    logging.info(f"Ended up at {position} facing {TURNS[facing]['facing']} for a password of {password}")
