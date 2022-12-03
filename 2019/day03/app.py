import argparse
import os

def points_steps(route):
    position = (0, 0)
    steps = 0
    movements = {'R': (1,0), 'L': (-1,0), 'U': (0,1), 'D': (0,-1)}
    points = {}
    for p in route:
        x, y = movements[p[0]]
        for _ in range(p[1]):
            position = (position[0] + x, position[1] + y)
            steps += 1
            points[position] = steps
    return points

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    wires = [[(v[0], int(v[1:])) for v in l.split(',')] for l in file.read().strip().split('\n')]

##########
# part 1 #
##########
    points_0 = points_steps(wires[0])
    points_1 = points_steps(wires[1])

    intersections = [p for p in points_0 if p in points_1]
    print(min([abs(i[0]) + abs(i[1]) for i in intersections]))

##########
# part 2 #
##########
    print(min([points_0[i] + points_1[i] for i in intersections]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
