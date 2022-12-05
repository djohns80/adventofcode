import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = [int(l) for l in file.read().strip().split('\n')]

##########
# part 1 #
##########
    lines1 = lines.copy()
    position = 0
    jumps = 0
    while position >= 0 and position < len(lines1):
        jumps += 1
        offset = lines1[position]
        lines1[position] += 1
        position += offset
    print(jumps)

##########
# part 2 #
##########
    lines2 = lines.copy()
    position = 0
    jumps = 0
    while position >= 0 and position < len(lines2):
        jumps += 1
        offset = lines2[position]
        if offset >= 3:
            lines2[position] -= 1
        else:
            lines2[position] += 1
        position += offset
    print(jumps)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
