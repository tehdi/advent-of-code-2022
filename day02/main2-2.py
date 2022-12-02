ROCK =     { 'name': 'rock',     'symbol': 'A', 'score': 1, 'X': 'C', 'Y': 'A', 'Z': 'B' }
PAPER =    { 'name': 'paper',    'symbol': 'B', 'score': 2, 'X': 'A', 'Y': 'B', 'Z': 'C' }
SCISSORS = { 'name': 'scissors', 'symbol': 'C', 'score': 3, 'X': 'B', 'Y': 'C', 'Z': 'A' }

SYMBOLS = { 'A': ROCK, 'B': PAPER, 'C': SCISSORS }
EXPECTED_RESULTS = { 'X': 'I lose', 'Y': 'we draw', 'Z': 'I win' }

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    opponent_score = 0
    my_score = 0
    for line in input_data:
        opponent_symbol, my_symbol = line.split()
        opponent_move = SYMBOLS[opponent_symbol]
        opponent_score += opponent_move['score']

        my_move = SYMBOLS[opponent_move[my_symbol]]
        my_score += my_move['score']
        print(f"Expected result: {EXPECTED_RESULTS[my_symbol]}")

        if opponent_move == my_move:
            opponent_score += 3
            my_score += 3
            print(f"  Actual result: we draw. opponent's {opponent_move['name']} ties my {my_move['name']}. Scores: O={opponent_score} | M={my_score}")
        elif opponent_move['X'] == my_move['symbol']:
            opponent_score += 6
            print(f"  Actual result: I lose. opponent's {opponent_move['name']} beats my {my_move['name']}. Scores: O={opponent_score} | M={my_score}")
        elif my_move['X'] == opponent_move['symbol']:
            my_score += 6
            print(f"  Actual result: I win. opponent's {opponent_move['name']} loses to my {my_move['name']}. Scores: O={opponent_score} | M={my_score}")

    winner = 'tie' if opponent_score == my_score else 'opponent' if opponent_score > my_score else 'me'
    print(f"Final scores: O={opponent_score} | M={my_score} || Winner: {winner}")
