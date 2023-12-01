import argparse
import os
import numpy as np
import scipy.ndimage as ndi

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    cubes = [list(map(int, l.split(','))) for l in file.read().splitlines()]
    directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]

##########
# part 1 #
##########
    print(sum(int([c[0] + dx, c[1] + dy, c[2] + dz] not in cubes) for c in cubes for dx,dy,dz in directions))

##########
# part 2 #
##########
    np_cubes = np.array(cubes)
    spaces = np.zeros(np_cubes.max(axis=0) + 1)
    i, j, k = np_cubes.T
    spaces[i, j, k] = 1
    spaces = ndi.binary_fill_holes(spaces)
    cubes = set(zip(*np.where(spaces)))
    print(sum(int((c[0] + dx, c[1] + dy, c[2] + dz) not in cubes) for c in cubes for dx,dy,dz in directions))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
