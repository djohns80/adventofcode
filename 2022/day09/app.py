import argparse
import math
import os
from collections import defaultdict

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    motions = [m.split() for m in file.read().strip().split('\n')]

    movements = {'L': -1 + 0j, 'R': 1 + 0j, 'U': 0 + 1j, 'D': 0 - 1j}

##########
# part 1 #
##########
    h_pos = 0 + 0j
    t_pos = 0 + 0j
    t_visits = defaultdict(int)
    t_visits[t_pos] += 1
    for m in motions:
        for _ in range(int(m[1])):
            h_pos += movements[m[0]]
            while abs(h_pos - t_pos) > math.sqrt(2):
                correction = 0 + 0j
                if (h_pos - t_pos).real > 0:
                    correction += movements['R']
                elif (h_pos - t_pos).real < 0:
                    correction += movements['L']
                if (h_pos - t_pos).imag > 0:
                    correction += movements['U']
                elif (h_pos - t_pos).imag < 0:
                    correction += movements['D']
                t_pos += correction
            t_visits[t_pos] += 1
    print(len(t_visits))

##########
# part 2 #
##########
    knots = [0 + 0j] * 10
    t_visits = defaultdict(int)
    t_visits[knots[-1]] += 1
    for m in motions:
        for _ in range(int(m[1])):
            knots[0] += movements[m[0]]
            for k in range(len(knots)-1):
                while abs(knots[k] - knots[k+1]) > math.sqrt(2):
                    correction = 0 + 0j
                    if (knots[k] - knots[k+1]).real > 0:
                        correction += movements['R']
                    elif (knots[k] - knots[k+1]).real < 0:
                        correction += movements['L']
                    if (knots[k] - knots[k+1]).imag > 0:
                        correction += movements['U']
                    elif (knots[k] - knots[k+1]).imag < 0:
                        correction += movements['D']
                    knots[k+1] += correction
            t_visits[knots[-1]] += 1
    print(len(t_visits))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
