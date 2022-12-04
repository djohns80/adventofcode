import argparse
import os
import re
from collections import Counter

def mod(n, d):
    t = n % d
    return d if t == 0 else t

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().strip().split('\n')
    rooms = []
    for l in lines:
        match = re.match(r'^(?P<name>(?:[a-z]+-)*[a-z]+)-(?P<sector>\d+)\[(?P<checksum>[a-z]+)\]$', l)
        if match:
            rooms.append(match.groupdict())

##########
# part 1 #
##########
    real_rooms = []
    for r in rooms:
        counts = Counter(list(r['name'].replace('-','')))
        counts_list = list(counts.items())
        counts_list.sort(key=lambda k: k[0])
        counts_list.sort(key=lambda k: k[1], reverse=True)
        if ''.join([c[0] for c in counts_list])[:5]== r['checksum']:
            real_rooms.append(r)
    print(sum([int(r['sector']) for r in real_rooms]))

##########
# part 2 #
##########

    real_rooms[0] = {'name': 'qzmt-zixmtkozy-ivhz', 'sector': '343', 'checksum': 'zimth'}
    for r in real_rooms:
        real_name = ''.join([' ' if ord(c) == 45 else chr(mod(ord(c)-96+int(r['sector']), 26) + 96) for c in list(r['name'])])
        if real_name == 'northpole object storage':
            print(r['sector'])
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
