import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    passphrases = file.read().strip().split('\n')

##########
# part 1 #
##########
    valid = [p for p in passphrases if len(p.split()) == len(set(p.split()))]
    print(len(valid))

##########
# part 2 #
##########
    sorted_chars = [' '.join([''.join(sorted(list(w))) for w in v.split()]) for v in valid]
    new_valid = [p for p in sorted_chars if len(p.split()) == len(set(p.split()))]
    print(len(new_valid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
