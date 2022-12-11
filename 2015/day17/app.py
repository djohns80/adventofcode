import argparse
import os
import itertools

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    containers = list(map(int, file.read().splitlines()))

    required = 150

##########
# part 1 #
##########
    counter = []
    for n in range(2, len(containers)):
        for p in itertools.combinations(containers, n):
            if sum(p) == required:
                counter.append(p)
    print(len(counter))

##########
# part 2 #
##########
    print(sum(1 for c in counter if len(c) == min(len(c) for c in counter)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
