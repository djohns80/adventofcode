import argparse
import os

def is_visible(grid, x, y):
    left = grid[y][x] > max(grid[y][:x])
    right = grid[y][x] > max(grid[y][x+1:])
    top = grid[y][x] > max([c[x] for c in grid][:y])
    bottom = grid[y][x] > max([c[x] for c in grid][y+1:])
    return any([left, right, top, bottom])

def get_view(grid, x, y):
    for i, v in enumerate(reversed(grid[y][:x])):
        if v >= grid[y][x]:
            left = i+1
            break
    else:
        left = x
    for i, v in enumerate(grid[y][x+1:]):
        if v >= grid[y][x]:
            right = i+1
            break
    else:
        right = len(grid[0])-1-x
    for i, v in enumerate(reversed([c[x] for c in grid][:y])):
        if v >= grid[y][x]:
            up = i+1
            break
    else:
        up = y
    for i, v in enumerate([c[x] for c in grid][y+1:]):
        if v >= grid[y][x]:
            down = i+1
            break
    else:
        down = len(grid)-1-y
    return left * right * up * down

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    grid = [list(map(int,list(l))) for l in file.read().strip().split('\n')]

##########
# part 1 #
##########
    perimeter = 2 * (len(grid) + len(grid[0])) - 4
    print(perimeter + sum(int(is_visible(grid, x, y)) for y in range(1, len(grid)-1) for x in range(1, len(grid[0])-1)))

###########
## part 2 #
###########
    print(max(get_view(grid, x, y) for y in range(1, len(grid)-1) for x in range(1, len(grid[0])-1)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
