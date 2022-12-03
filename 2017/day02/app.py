import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    spreadsheet = [[int(v) for v in l.split()] for l in file.read().strip().split('\n')]

##########
# part 1 #
##########
    checksums = [max(s)- min(s) for s in spreadsheet]
    print(sum(checksums))

##########
# part 2 #
##########
    div_values = [int(p[0] / p[1]) for s in spreadsheet for p in [sorted([s1, s2], reverse=True) for n1, s1 in enumerate(s) for n2, s2 in enumerate(s) if n1 > n2] if p[0] % p[1] == 0]
    print(sum(div_values))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
