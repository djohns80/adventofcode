import argparse
import os
from collections import defaultdict

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().strip().split('\n')

##########
# part 1 #
##########
    counts = defaultdict(lambda: defaultdict(int))
    for l in lines:
        for n, v in enumerate(list(l)):
            counts[n][v] += 1
    print(''.join([sorted(c.items(), key=lambda k_v: k_v[1], reverse=True)[0][0] for n, c in counts.items()]))

##########
# part 2 #
##########
    print(''.join([sorted(c.items(), key=lambda k_v: k_v[1])[0][0] for n, c in counts.items()]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
