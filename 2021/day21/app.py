from collections import defaultdict, Counter

if __name__ == '__main__':
#    input = [4, 8]
    input = [8, 3]

##########
# part 1 #
##########
    position = input.copy()
    score = [0, 0]
    die = 0
    rolls = 0
    player = 0
    while max(score) < 1000:
        for r in range(3):
            die = die % 100 + 1
            position[player] += die
            rolls += 1
        position[player] = (position[player] - 1) % 10 + 1
        score[player] += position[player]
        player = int(not player)
    print(rolls * min(score))

##########
# part 2 #
##########
    position = input.copy()
    player = 0
    universes = defaultdict(int)
    universes[(position[0], position[1], 0, 0)] = 1
    possible_rolls = Counter([d1+d2+d3 for d1 in range(1,4) for d2 in range(1,4) for d3 in range(1,4)])
    in_progress = True
    while in_progress:
        in_progress = False
        next = defaultdict(int)
        for key in universes:
            if max(key[2:]) < 21:
                in_progress = True
                for roll in possible_rolls:
                    pos = (key[player] - 1 + roll) % 10 + 1
                    if player == 0:
                        next[(pos, key[1], key[2]+pos, key[3])] += possible_rolls[roll] * universes[key]
                    elif player == 1:
                        next[(key[0], pos, key[2], key[3]+pos)] += possible_rolls[roll] * universes[key]
            else:
                if universes[key]:
                    next[key] += universes[key]
        universes = next
        player = int(not player)
    print(max(sum([v for k,v in universes.items() if k[2] >= 21]), sum([v for k,v in universes.items() if k[3] >= 21])))
