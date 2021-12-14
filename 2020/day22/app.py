
def play_game(hands):
    while hands[0] and hands[1]:
        cards = (hands[0].pop(0), hands[1].pop(0))
        winner = 0 if cards[0] > cards[1] else 1
        hands[winner].extend([cards[0 if winner == 0 else 1],cards[1 if winner == 0 else 0]])
    result = [(n+1, h) for n, h in enumerate(hands) if h][0]
    return f'player{result[0]}', result[1]

def play_recursive_game(hands):
    rounds = []
    while hands[0] and hands[1]:
        if hands in rounds:
            return 0, hands[0]
        rounds.append((hands[0].copy(), hands[1].copy()))
        cards = (hands[0].pop(0), hands[1].pop(0))
        sub_game = all([cards[n] <= len(h) for n, h in enumerate(hands)])
        if sub_game:
            winner, _ = play_recursive_game((hands[0][:cards[0]].copy(), hands[1][:cards[1]].copy()))
        else:
            winner = 0 if cards[0] > cards[1] else 1
        hands[winner].extend([cards[0 if winner == 0 else 1],cards[1 if winner == 0 else 0]])
    result = [(n, h) for n, h in enumerate(hands) if h][0]
    return result[0], result[1]

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.read()
    p1_hand, p2_hand = lines.split('\n\n')
    p1_hand = [int(c) for c in p1_hand.splitlines()[1:]]
    p2_hand = [int(c) for c in p2_hand.splitlines()[1:]]

##########
# part 1 #
##########
    _, hand = play_game((p1_hand.copy(), p2_hand.copy()))
    scores = [abs(n-len(hand)) * v for n, v in enumerate(hand)]
    print(sum(scores))

##########
# part 2 #
##########
    _, hand = play_recursive_game((p1_hand.copy(), p2_hand.copy()))
    scores = [abs(n-len(hand)) * v for n, v in enumerate(hand)]
    print(sum(scores))
