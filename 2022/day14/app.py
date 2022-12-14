import argparse
import os
from collections import defaultdict

def move(g, p, h):
    if p.imag >= h + 2:
        return None
    for t in [0 + 1j, -1 + 1j, 1 + 1j]:
        if g[p + t] == '.':
            return p + t
    return None

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = file.read().splitlines()
    grid = defaultdict(lambda: '.')
    y_max = 0
    for d in data:
        end_points = [list(map(int, p.split(','))) for p in d.split(' -> ')]
        lines = list(zip(end_points, end_points[1:]))
        for l in lines:
            x_range = sorted([l[0][0], l[1][0]])
            y_range = sorted([l[0][1], l[1][1]])
            if  y_range[1] > y_max:
                y_max = y_range[1]
            for y in range(y_range[0], y_range[1]+1):
                for x in range(x_range[0], x_range[1]+1):
                    grid[x + (y * 1j)] = '#'

##########
# part 1 #
##########
    n1 = 0
    part1  = grid.copy()
    while True:
        pos = 500 + 0j
        for _ in range(y_max + 1):
            new_pos = move(part1, pos, y_max)
            if new_pos:
                pos = new_pos
            else:
                break
        if pos.imag > y_max:
            break
        part1[pos] = 'o'
        n1 += 1
    print(n1)

##########
# part 2 #
##########
    n2 = 0
    part2  = grid.copy()
    while True:
        pos = 500 + 0j
        for _ in range(y_max + 1):
            new_pos = move(part2, pos, y_max)
            if new_pos:
                pos = new_pos
            else:
                break
        part2[pos] = 'o'
        n2 += 1
        if pos == 500 + 0j:
            break
    print(n2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
