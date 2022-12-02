import os
from collections import defaultdict

def main():
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'input'), 'r', encoding='utf-8')
    strategy = [l.strip().split(' ') for l in file.readlines()]
    points = {
        'R': 1,
        'P': 2,
        'S': 3,

        'W': 6,
        'L': 0,
        'D': 3
    }

##########
# part 1 #
##########
    map = {
        'A': 'R',
        'B': 'P',
        'C': 'S',

        'X': 'R',
        'Y': 'P',
        'Z': 'S',
    }
    results = defaultdict(int)
    results[('R','R')] = 'D'
    results[('R','P')] = 'W'
    results[('R','S')] = 'L'
    results[('P','R')] = 'L'
    results[('P','P')] = 'D'
    results[('P','S')] = 'W'
    results[('S','R')] = 'W'
    results[('S','P')] = 'L'
    results[('S','S')] = 'D'
    scores = [points[results[(map[s[0]], map[s[1]])]] + points[map[s[1]]] for s in strategy]
    print(sum(scores))

##########
# part 2 #
##########
    map = {
        'A': 'R',
        'B': 'P',
        'C': 'S',

        'X': 'L',
        'Y': 'D',
        'Z': 'W',
    }
    results = defaultdict(int)
    results[('R','D')] = 'R'
    results[('R','W')] = 'P'
    results[('R','L')] = 'S'
    results[('P','L')] = 'R'
    results[('P','D')] = 'P'
    results[('P','W')] = 'S'
    results[('S','W')] = 'R'
    results[('S','L')] = 'P'
    results[('S','D')] = 'S'
    scores = [points[results[(map[s[0]], map[s[1]])]] + points[map[s[1]]] for s in strategy]
    print(sum(scores))

if __name__ == '__main__':
    main()