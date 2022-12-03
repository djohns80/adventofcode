import argparse
import os
from collections import defaultdict

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    directions = list(file.read())

##########
# part 1 #
##########
    position = (0,0)
    visits = defaultdict(int)
    visits[position] += 1
    for d in directions:
        if d == '^':
            position = (position[0], position[1]+1)
        elif d == 'v':
            position = (position[0], position[1]-1)
        elif d == '>':
            position = (position[0]+1, position[1])
        elif d == '<':
            position = (position[0]-1, position[1])
        visits[position] += 1
    print(len(visits))

##########
# part 2 #
##########
    people = ['santa', 'robot']
    position = {
        people[0]: (0,0),
        people[1]: (0,0)
    }
    visits = defaultdict(int)
    for p in people:
        visits[position[p]] += 1
    for n, d in enumerate(directions):
        person = n % 2
        if d == '^':
            position[people[person]] = (position[people[person]][0], position[people[person]][1]+1)
        elif d == 'v':
            position[people[person]] = (position[people[person]][0], position[people[person]][1]-1)
        elif d == '>':
            position[people[person]] = (position[people[person]][0]+1, position[people[person]][1])
        elif d == '<':
            position[people[person]] = (position[people[person]][0]-1, position[people[person]][1])
        visits[position[people[person]]] += 1
    print(len(visits))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
