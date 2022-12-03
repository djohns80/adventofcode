import argparse
import os
from collections import Counter

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    box_ids = file.read().strip().split('\n')

##########
# part 1 #
##########
    twos = 0
    threes = 0
    for b in box_ids:
        counts = Counter(list(b))
        if any([k for k,v in counts.items() if v == 2]):
            twos += 1
        if any([k for k,v in counts.items() if v == 3]):
            threes +=1
    print(twos * threes)


##########
# part 2 #
##########
    pairs = [[b1, b2] for n1, b1 in enumerate(box_ids) for n2, b2 in enumerate(box_ids) if n1 > n2]
    for p in pairs:
        common = ''.join([p[0][i] for i in range(len(p[0])) if int(p[0][i] != p[1][i]) == 0])
        if len(common) == len(p[0]) - 1:
            print(common)
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)