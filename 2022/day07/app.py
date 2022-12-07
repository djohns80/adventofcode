import argparse
import os
from collections import defaultdict

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    commands = file.read().strip().split('\n')

    directories = defaultdict(int)
    cwd = []
    for l in commands:
        if l == '$ cd ..':
            cwd.pop()
        elif l.startswith('$ cd'):
            cwd.append((''.join(cwd) + '/' + l.split(' ')[-1]).replace('//','/'))
        elif l[0].isdigit():
            for d in cwd:
                directories[d] += int(l.split(' ')[0])

##########
# part 1 #
##########
    print(sum(s for s  in directories.values() if s <= 100000))

##########
# part 2 #
##########
    required_space = 30000000 - (70000000 - directories['/'])
    print(min(s for s in directories.values() if s >= required_space))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
