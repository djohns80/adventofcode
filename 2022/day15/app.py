import argparse
import os
import re

def get_manhattan(a, b):
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))

def get_perimeter(a, r, m):
    boundary = set([(v * s[0] + ((r + 1 - v) * s[1]) * 1j) for s in [(1, 1), (1, -1), (-1, 1), (-1, -1)] for v in range(r + 2)])
    return set([a + b for b in boundary if (a + b).real <= m and (a + b).imag <= m and (a + b).real >= 0 and (a + b).imag >= 0])

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = [
        {
            'S': int(r.groupdict()['xs']) + (int(r.groupdict()['ys']) * 1j),
            'B': int(r.groupdict()['xb']) + (int(r.groupdict()['yb']) * 1j),
            'M': get_manhattan(int(r.groupdict()['xs']) + (int(r.groupdict()['ys']) * 1j), int(r.groupdict()['xb']) + (int(r.groupdict()['yb']) * 1j))
        } for r in re.finditer(r'Sensor at x=(?P<xs>-?\d+), y=(?P<ys>-?\d+): closest beacon is at x=(?P<xb>-?\d+), y=(?P<yb>-?\d+)', file.read())]

##########
# part 1 #
##########
    x_min = int(min([d['S'].real - get_manhattan(d['B'], d['S']) for d in data]))
    x_max = int(max([d['S'].real + get_manhattan(d['B'], d['S']) for d in data]))
    y = 10 if input_file =='sample' else 2000000
    print(sum(int(any([get_manhattan(x + (y * 1j), d['S']) <= d['M'] for d in data]) and sum(1 for d in data if d['B'] == x + (y * 1j)) == 0) for x in range(x_min, x_max + 1)))

##########
# part 2 #
###########
    max_value = 20 if input_file =='sample' else 4000000
    for d in data:
        for p in get_perimeter(d['S'], d['M'], max_value):
            if all([get_manhattan(od['S'], p) > od['M'] for od in [t for t in data if t != d]]):
                print(int((p.real * 4000000) + p.imag))
                break
        else:
            continue
        break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
