ROCK =     { 'name': 'rock',     'score': 1, 'beats': 'C', 'beaten_by': 'B' }
PAPER =    { 'name': 'paper',    'score': 2, 'beats': 'A', 'beaten_by': 'C' }
SCISSORS = { 'name': 'scissors', 'score': 3, 'beats': 'B', 'beaten_by': 'A' }

SYMBOLS = { 'A': ROCK, 'B': PAPER, 'C': SCISSORS }

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    opponent_score = 0
    my_score = 0
    for line in input_data:
        opponent_symbol, my_symbol = line.split()
        opponent_move = SYMBOLS[opponent_symbol]
        opponent_score += opponent_move['score']
        if my_symbol == 'X':  # lose
            my_move = SYMBOLS[opponent_move['beats']]
            my_score += my_move['score']
            opponent_score += 6
            print(f"I should lose so I'm picking {my_move['name']} vs my opponent's {opponent_move['name']}")
            print(f"  Result: opponent's {opponent_move['name']} beats my {my_move['name']}. Scores: O={opponent_score} | M={my_score}")
        elif my_symbol == 'Y':  # draw
            my_move = opponent_move
            my_score += my_move['score'] + 3
            opponent_score += 3
            print(f"I should draw so I'm picking {my_move['name']} vs my opponent's {opponent_move['name']}")
            print(f"  Result: opponent's {opponent_move['name']} ties my {my_move['name']}. Scores: O={opponent_score} | M={my_score}")
        else:  # Z = win
            my_move = SYMBOLS[opponent_move['beaten_by']]
            my_score += my_move['score']
            my_score += 6
            print(f"I should win so I'm picking {my_move['name']} vs my opponent's {opponent_move['name']}")
            print(f"  Result: opponent's {opponent_move['name']} loses to my {my_move['name']}. Scores: O={opponent_score} | M={my_score}")

    winner = 'tie' if opponent_score == my_score else 'opponent' if opponent_score > my_score else 'me'
    print(f"Final scores: O={opponent_score} | M={my_score} || Winner: {winner}")
