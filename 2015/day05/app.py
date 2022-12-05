import argparse
import os
import re

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    names = file.read().strip().split('\n')

##########
# part 1 #
##########
    print(len([
        n for n in names
        if not any(d in n for d in ['ab', 'cd', 'pq', 'xy']) and
        len([v for v in n if v in 'aeiou']) >= 3 and
        any([i == j for i, j in zip(list(n), list(n[1:]))])
    ]))

##########
# part 2 #
##########
    print(len([
        n for n in names
        if len(re.findall(r'([a-z]{2}).*\1', n)) and
        re.findall(r'([a-z]).\1', n)
    ]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
