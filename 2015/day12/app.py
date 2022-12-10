import argparse
import json
import os
import re

def n(j):
    if isinstance(j, int):
        return j
    if isinstance(j, list):
        return sum([n(i) for i in j])
    if not isinstance(j, dict):
        return 0
    if 'red' in j.values():
        return 0
    return n(list(j.values()))

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = file.read()

##########
# part 1 #
##########
    match = re.findall(r'-?\d+', data)
    print(sum(map(int, match)))

##########
# part 2 #
##########
    print(n(json.loads(data)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
