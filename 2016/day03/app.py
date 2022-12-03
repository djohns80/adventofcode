import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    triangles = [[int(s) for s in l.split()] for l in file.read().strip().split('\n')]

##########
# part 1 #
##########
    valid_count = 0
    for t in triangles:
        sorted_t = sorted(t)
        if sorted_t[0] + sorted_t[1] > sorted_t[2]:
            valid_count += 1
    print(valid_count)

##########
# part 2 #
##########
    valid_count = 0
    for i in range(0, len(triangles), 3):
        for j in range(3):
            sorted_t = sorted([triangles[i][j], triangles[i+1][j], triangles[i+2][j]])
            if sorted_t[0] + sorted_t[1] > sorted_t[2]:
                valid_count += 1
    print(valid_count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
