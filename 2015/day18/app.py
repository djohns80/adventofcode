import argparse
import os

def count_neighbours(data, x, y):
    return sum([
        data[(x - 1, y - 1)] if (x - 1, y - 1) in data else 0,
        data[(x,     y - 1)] if (x,     y - 1) in data else 0,
        data[(x + 1, y - 1)] if (x + 1, y - 1) in data else 0,
        data[(x - 1, y)]     if (x - 1, y)     in data else 0,
        data[(x + 1, y)]     if (x + 1, y)     in data else 0,
        data[(x - 1, y + 1)] if (x - 1, y + 1) in data else 0,
        data[(x,     y + 1)] if (x,     y + 1) in data else 0,
        data[(x + 1, y + 1)] if (x + 1, y + 1) in data else 0
    ])

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().splitlines()
    grid = {}
    for y, l in enumerate(lines):
        for x, v in enumerate(l):
            grid[(x,y)] = 1 if v == '#' else 0

##########
# part 1 #
##########
#    for _ in range(100):
#        new_grid = {}
#        for c, v in grid.items():
#            if v == 1:
#                if count_neighbours(grid, c[0], c[1]) in [2, 3]:
#                    new_grid[c] = 1
#                else:
#                    new_grid[c] = 0
#            elif v == 0:
#                if count_neighbours(grid, c[0], c[1]) == 3:
#                    new_grid[c] = 1
#                else:
#                    new_grid[c] = 0
#        grid = new_grid.copy()
#    print(sum(grid[(x, y)] for y, l in enumerate(lines) for x, _ in enumerate(l)))

##########
# part 2 #
##########
    for _ in range(100):
        new_grid = {}
        for c, v in grid.items():
            if c in [(0, 0), (len(lines) - 1, 0), (0, len(lines[0]) - 1), (len(lines) - 1, len(lines[0]) - 1)]:
                new_grid[c] = 1
            elif v == 1:
                if count_neighbours(grid, c[0], c[1]) in [2, 3]:
                    new_grid[c] = 1
                else:
                    new_grid[c] = 0
            elif v == 0:
                if count_neighbours(grid, c[0], c[1]) == 3:
                    new_grid[c] = 1
                else:
                    new_grid[c] = 0
        grid = new_grid.copy()
    print(sum(grid[(x, y)] for y, l in enumerate(lines) for x, _ in enumerate(l)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
