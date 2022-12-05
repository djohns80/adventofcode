import argparse
import os
import re
from collections import defaultdict
from copy import deepcopy

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.readlines()

    stack_rows = []
    moves = []
    for l in lines:
        if l.strip() == '':
            pass
        elif l.strip().startswith('['):
            stack_rows.append(l.strip('\n'))
        elif l.strip().startswith('move'):
            match = re.match(r'^move\s(?P<move>\d+)\sfrom\s(?P<from>\d+)\sto\s(?P<to>\d+)', l)
            if match:
                moves.append({k: int(v) for k,v in match.groupdict().items()})
        else:
            stack_count = int(l.strip('\n').split()[-1])
    stacks = defaultdict(list)
    for s in reversed(stack_rows):
        for n in range(1, len(s), 4):
            col = int((n-1)/4)
            if s[n] != ' ':
                stacks[col].append(s[n])
    assert(len(stacks) == stack_count)

##########
# part 1 #
##########
    stacks1 = deepcopy(stacks)
    for m in moves:
        for n in range(m['move']):
            stacks1[m['to']-1].append(stacks1[m['from']-1].pop())
    print(''.join([s[-1] for s in stacks1.values()]))

##########
# part 2 #
##########
    stacks2 = deepcopy(stacks)
    for m in moves:
        pops = []
        for n in range(m['move']):
            pops.append(stacks2[m['from']-1].pop())
        stacks2[m['to']-1].extend(reversed(pops))
    print(''.join([s[-1] for s in stacks2.values()]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
