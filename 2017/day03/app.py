import argparse
import os
from collections import defaultdict

def get_surrounding_squares(grid, cell):
    TL = grid[(cell[0]-1,cell[1]+1)]
    TR = grid[(cell[0]+1,cell[1]+1)]
    BL = grid[(cell[0]-1,cell[1]-1)]
    BR = grid[(cell[0]+1,cell[1]-1)]
    L = grid[(cell[0]-1,cell[1])]
    R = grid[(cell[0]+1,cell[1])]
    T = grid[(cell[0],cell[1]+1)]
    B = grid[(cell[0],cell[1]-1)]
    return TL + TR + BL + BR + L + R + T + B

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data_square = int(file.read().strip())

##########
# part 1 #
##########
    position = (0, 0)
    odd_sq = 1
    value = 1
    while True:
        odd_sq += 2
        i = 1
        while value < odd_sq ** 2:
            value += 1
            if i == 1:
                position = (position[0] + 1, position[1])
            elif i <= odd_sq - 1:
                position = (position[0], position[1] + 1)
            elif i <= (odd_sq - 1) * 2:
                position = (position[0] - 1, position[1])
            elif i <= (odd_sq - 1) * 3:
                position = (position[0], position[1] - 1)
            elif i <= (odd_sq - 1) * 4:
                position = (position[0] + 1, position[1])
            i += 1
            if value == data_square:
                break
        if value == data_square:
            break
    print(abs(position[0]) + abs(position[1]))

##########
# part 2 #
##########
    values = defaultdict(int)
    position = (0, 0)
    odd_sq = 1
    value = 1
    values[position] = value
    while True:
        odd_sq += 2
        i = 1
        while value < odd_sq ** 2:
            value += 1
            if i == 1:
                position = (position[0] + 1, position[1])
            elif i <= odd_sq - 1:
                position = (position[0], position[1] + 1)
            elif i <= (odd_sq - 1) * 2:
                position = (position[0] - 1, position[1])
            elif i <= (odd_sq - 1) * 3:
                position = (position[0], position[1] - 1)
            elif i <= (odd_sq - 1) * 4:
                position = (position[0] + 1, position[1])
            i += 1
            values[position] = get_surrounding_squares(values, position)
            if values[position] > data_square:
                break
        if values[position] > data_square:
            break
    print(values[position])
#
#
#
#    get_surrounding_squares(values, (0,0))

#    values = defaultdict(int)
#    position = (0, 0)
#    odd_sq = 1
#    value = 1
#    values[position] = value
#    while True:
#        odd_sq += 2
#        i = 1
#        while value < odd_sq ** 2:
#            value += 1
#            if i == 1:
#                position = (position[0] + 1, position[1])
#            elif i <= odd_sq - 1:
#                position = (position[0], position[1] + 1)
#            elif i <= (odd_sq - 1) * 2:
#                position = (position[0] - 1, position[1])
#            elif i <= (odd_sq - 1) * 3:
#                position = (position[0], position[1] - 1)
#            elif i <= (odd_sq - 1) * 4:
#                position = (position[0] + 1, position[1])
#            i += 1
#            values[position] = value
#            if value == data_square:
#                part1 = position
#        if value >= data_square:
#            break
#    print(abs(part1[0]) + abs(part1[1]))










#https://oeis.org/A141481
#https://oeis.org/A141481/b141481.txt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)

