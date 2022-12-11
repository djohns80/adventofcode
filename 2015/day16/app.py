import argparse
import os
import re

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = [m.groupdict() for m in re.finditer(r'Sue\s(?P<sue_no>\d+):\s(?P<p1>[a-z]+):\s(?P<v1>\d+),\s(?P<p2>[a-z]+):\s(?P<v2>\d+),\s(?P<p3>[a-z]+):\s(?P<v3>\d+)', file.read())]
    aunts = {int(d['sue_no']): {d['p1']: int(d['v1']), d['p2']: int(d['v2']), d['p3']: int(d['v3'])} for d in data}

##########
# part 1 #
##########
    matches = []
    for a, d in aunts.items():
        if 'children' in d and d['children'] != 3:
            continue
        if 'cats' in d and d['cats'] != 7:
            continue
        if 'samoyeds' in d and d['samoyeds'] != 2:
            continue
        if 'pomeranians' in d and d['pomeranians'] != 3:
            continue
        if 'akitas' in d and d['akitas'] != 0:
            continue
        if 'vizslas' in d and d['vizslas'] != 0:
            continue
        if 'goldfish' in d and d['goldfish'] != 5:
            continue
        if 'trees' in d and d['trees'] != 3:
            continue
        if 'cars' in d and d['cars'] != 2:
            continue
        if 'perfumes' in d and d['perfumes'] != 1:
            continue
        matches.append(a)
    print(matches)

##########
# part 2 #
##########
    matches = []
    for a, d in aunts.items():
        if 'children' in d and d['children'] != 3:
            continue
        if 'cats' in d and d['cats'] <= 7:
            continue
        if 'samoyeds' in d and d['samoyeds'] != 2:
            continue
        if 'pomeranians' in d and d['pomeranians'] >= 3:
            continue
        if 'akitas' in d and d['akitas'] != 0:
            continue
        if 'vizslas' in d and d['vizslas'] != 0:
            continue
        if 'goldfish' in d and d['goldfish'] >= 5:
            continue
        if 'trees' in d and d['trees'] <= 3:
            continue
        if 'cars' in d and d['cars'] != 2:
            continue
        if 'perfumes' in d and d['perfumes'] != 1:
            continue
        matches.append(a)
    print(matches)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
