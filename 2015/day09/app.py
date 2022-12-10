import argparse
import os
import itertools

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = [l.split() for l in file.read().strip().split('\n')]
    distances = {}
    for l in lines:
        distances[(l[0], l[2])] = int(l[4])
        distances[(l[2], l[0])] = int(l[4])
    destinations = set([d[0] for d in distances])

##########
# part 1 #
##########
    print(min(sum(distances[(d1, d2)] for d1, d2  in zip(d_list, d_list[1:])) for d_list in itertools.permutations(destinations)))

##########
# part 2 #
##########
    print(max(sum(distances[(d1, d2)] for d1, d2  in zip(d_list, d_list[1:])) for d_list in itertools.permutations(destinations)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
