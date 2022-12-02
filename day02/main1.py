ROCK = { 'name': 'rock', 'score': 1, 'beats': 'scissors' }
PAPER = { 'name': 'paper', 'score': 2, 'beats': 'rock' }
SCISSORS = { 'name': 'scissors', 'score': 3, 'beats': 'paper' }

SYMBOLS = { 'A': ROCK, 'B': PAPER, 'C': SCISSORS, 'X': ROCK, 'Y': PAPER, 'Z': SCISSORS }

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    opponent_score = 0
    my_score = 0
    for line in input_data:
        opponent_symbol, my_symbol = line.split()
        opponent_move = SYMBOLS[opponent_symbol]
        my_move = SYMBOLS[my_symbol]
        opponent_score += opponent_move['score']
        my_score += my_move['score']
        if opponent_move == my_move:
            opponent_score += 3
            my_score += 3
            print(f"opponent's {opponent_move['name']} ties my {my_move['name']}. Scores: O={opponent_score} | M={my_score}")
        elif opponent_move['beats'] == my_move['name']:
            opponent_score += 6
            print(f"opponent's {opponent_move['name']} beats my {my_move['name']}. Scores: O={opponent_score} | M={my_score}")
        elif my_move['beats'] == opponent_move['name']:
            my_score += 6
            print(f"opponent's {opponent_move['name']} loses to my {my_move['name']}. Scores: O={opponent_score} | M={my_score}")
    winner = 'tie' if opponent_score == my_score else 'opponent' if opponent_score > my_score else 'me'
    print(f"Final scores: O={opponent_score} | M={my_score} || Winner: {winner}")
