import argparse
import os
import re
from random import shuffle

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().strip().splitlines()
    replacements = []
    for l in lines:
        if '=>' in l:
            k, _, v = l.split()
            replacements.append((k, v))
        elif l != '':
            molecule = l

##########
# part 1 #
##########
    results = set()
    for rk, rv in replacements:
        for m in re.finditer(rk, molecule):
            results.add(''.join([molecule[:m.start()], rv, molecule[m.start() + len(rk):]]))
    print(len(results))

##########
# part 2 #
##########
    ### TODO: Understand part 2
    target = molecule
    part2 = 0
    while target != 'e':
        tmp = target
        for a, b in replacements:
            if b not in target:
                continue
            target = target.replace(b, a, 1)
            part2 += 1
        if tmp == target:
            target = molecule
            part2 = 0
            shuffle(replacements)
    print(part2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
