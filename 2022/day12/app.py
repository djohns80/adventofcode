import argparse
import os

def move(data, p1, p2):
    return (
        p2 in data and
        (
            (data[p1] == 'E' and data[p2] in ['y', 'z']) or
            (data[p2] == 'S' and data[p1] in ['a', 'b']) or
            (data[p2] != 'S' and data[p1] != 'E' and ord(data[p1]) - ord(data[p2]) <= 1)
        )
    )

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().splitlines()

    grid = {(i + j * 1j): c for j, l in enumerate(lines) for i, c in enumerate(l)}
    start = [k for k, v in grid.items() if v == 'S'][0]
    end = [k for k, v in grid.items() if v == 'E'][0]

    paths = {end: 0}
    queue = [end]

    while queue:
        p1 = queue.pop(0)
        for p in filter(lambda p2: move(grid, p1, p2), [p1 - (1 + 0j), p1 + (1 + 0j), p1 - (0 + 1j), p1 + (0 + 1j)]):
            if p not in paths:
                paths[p] = paths[p1] + 1
                queue.append(p)

##########
# part 1 #
##########
    print(paths[start])

##########
# part 2 #
##########
    print(sorted(paths[p] for p in paths if grid[p] in ['S', 'a'])[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
