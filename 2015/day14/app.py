import argparse
import os
from collections import defaultdict

def state(i, s, d, r):
    seconds = (i // (d + r)) * d
    remainder = i % (d + r)
    if remainder > d:
        seconds += d
    else:
        seconds += remainder
    return seconds * s

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = [l.split() for l in file.read().strip().split('\n')]
    data = {l[0]: (int(l[3]), int(l[6]), int(l[13])) for l in lines}

##########
# part 1 #
##########
    s = 2503
    distances = defaultdict(int)
    points = defaultdict(int)
    for i in range(1, s+1):
        for r, d in data.items():
            distances[r] = state(i, *d)
        for k,v in distances.items():
            if v == max(distances.values()):
                points[k] += 1
    print(max(distances.values()))

##########
# part 2 #
##########
    print(max(points.values()))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
