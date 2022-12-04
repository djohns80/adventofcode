import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    pairs = [[[int(n) for n in s.split('-')] for s in l.split(',')] for l in file.read().strip().split('\n')]

##########
# part 1 #
##########
    full_overlap = [p for p in pairs if (p[0][0] >= p[1][0] and p[0][1] <= p[1][1]) or (p[1][0] >= p[0][0] and p[1][1] <= p[0][1])]
    print(len(full_overlap))

##########
# part 2 #
##########
    overlaps = [p for p in pairs if len(range(max(p[0][0], p[1][0]), min(p[0][1], p[1][1]) + 1)) != 0]
    print(len(overlaps))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)