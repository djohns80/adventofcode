import argparse
import os
from collections import defaultdict

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    coords = [tuple(map(int, l.split(', '))) for l in file.read().strip().split('\n')]
    max_x = max([c[0] for c in coords])
    max_y = max([c[1] for c in coords])

##########
# part 1 #
##########
    region_sizes = defaultdict(int)
    infinite_ids = set()
    for i in range(max_x + 1):
        for j in range(max_y + 1):
            min_dists = sorted([(abs(x - i) + abs(y - j), n) for n, (x, y) in enumerate(coords)])
            if len(min_dists) == 1 or min_dists[0][0] != min_dists[1][0]:
                n = min_dists[0][1]
                region_sizes[n] += 1
                if i == 0 or i == max_x or j == 0 or j == max_y:
                    infinite_ids.add(n)
    print(max(v for k, v in region_sizes.items() if k not in infinite_ids))

##########
# part 2 #
##########
    print(sum(int(sum(abs(x - i) + abs(y - j) for x, y in coords) < 10000) for i in range(max_x + 1) for j in range(max_y + 1)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
