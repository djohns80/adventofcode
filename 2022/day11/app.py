import argparse
import math
import os
from collections import defaultdict
from copy import deepcopy

def operation(o, v):
    match o[0]:
        case '*':
            if o[1] == 'old':
                return v * v
            else:
                return v * int(o[1])
        case '+':
            return v + int(o[1])
        case _:
            return v

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().splitlines()

    block_lines = 7
    items = {}
    operations = {}
    tests = {}

    for n in range((len(lines)+1) // block_lines):
        items[n] = list(map(int, lines[n*block_lines + 1].replace(',','').split()[2:]))
        operations[n] = lines[n*block_lines + 2].split()[4:]
        tests[n] = list(map(int, [lines[n*block_lines + 3].split()[-1], lines[n*block_lines + 4].split()[-1], lines[n*block_lines + 5].split()[-1]]))

###########
## part 1 #
###########
    inspections = defaultdict(int)
    items_copy = deepcopy(items)
    for _ in range(20):
        for m, v in items_copy.items():
            for i in v:
                new_i = operation(operations[m], i) // 3
                new_m = tests[m][1] if new_i % tests[m][0] == 0 else tests[m][2]
                items_copy[new_m].append(new_i)
                inspections[m] += 1
            items_copy[m] = []
    print(math.prod(sorted(inspections.values(), reverse=True)[:2]))

###########
## part 2 #
###########
    hcf = math.prod([v[0] for v in tests.values()]) # use hcf to increase performance
    inspections = defaultdict(int)
    items_copy = deepcopy(items)
    for _ in range(10000):
        for m, v in items_copy.items():
            for i in v:
                new_i = operation(operations[m], i)
                new_i = new_i % hcf
                new_m = tests[m][1] if new_i % tests[m][0] == 0 else tests[m][2]
                items_copy[new_m].append(new_i)
                inspections[m] += 1
            items_copy[m] = []
    print(math.prod(sorted(inspections.values(), reverse=True)[:2]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
