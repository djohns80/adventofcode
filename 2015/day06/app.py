import argparse
import os
import re
from collections import defaultdict

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().strip().split('\n')
    actions = []
    for l in lines:
        match = re.match(r'(?:turn)?\s?(?P<action>on|off|toggle)\s(?P<x1>\d+),(?P<y1>\d+)\sthrough\s(?P<x2>\d+),(?P<y2>\d+)$', l)
        if match:
            actions.append(match.groupdict())

##########
# part 1 #
##########
    lights = defaultdict(int)
    for a in actions:
        for y in range(int(a['y1']), int(a['y2'])+1):
            for x in range(int(a['x1']), int(a['x2'])+1):
                if a['action'] == 'on':
                    lights[(x,y)] = 1
                elif a['action'] == 'off':
                    lights[(x,y)] = 0
                elif a['action'] == 'toggle':
                    lights[(x,y)] = 0 if lights[(x,y)] == 1 else 1
    print(sum(lights.values()))

##########
# part 2 #
##########
    lights = defaultdict(int)
    for a in actions:
        for y in range(int(a['y1']), int(a['y2'])+1):
            for x in range(int(a['x1']), int(a['x2'])+1):
                if a['action'] == 'on':
                    lights[(x,y)] += 1
                elif a['action'] == 'off':
                    lights[(x,y)] = lights[(x,y)] - 1 if lights[(x,y)] > 1 else 0
                elif a['action'] == 'toggle':
                    lights[(x,y)] += 2
    print(sum(lights.values()))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
