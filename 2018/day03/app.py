import argparse
import os
import re

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().strip().split('\n')
    claims = []
    for l in lines:
        match = re.match(r'^#(?P<id>\d+)\s@\s(?P<left>\d+),(?P<top>\d+):\s(?P<width>\d+)x(?P<height>\d+)$', l)
        if match:
            claims.append({k: int(v) for k,v in match.groupdict().items()})

##########
# part 1 #
##########
    material = {}
    overlap_counts = {}
    for c in claims:
        overlap_counts[str(c['id'])] = 0
        for w in range(c['width']):
            for h in range(c['height']):
                position = (c['left'] + w, c['top'] + h)
                if position in material:
                    overlap_counts[str(c['id'])] += 1
                    if material[position] != 'X':
                        overlap_counts[material[position]] += 1
                    material[position] = 'X'
                else:
                    material[position] = str(c['id'])
    overlaps = [k for k, v in material.items() if v == 'X']
    print(len(overlaps))

##########
# part 2 #
##########
    print([k for k,v in overlap_counts.items() if v == 0][0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
