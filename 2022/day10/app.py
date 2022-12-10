import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    program = [(l[:4], l[5:]) for l in file.read().strip().split('\n')]

##########
# part 1 #
##########
    x = [1]
    for i in program:
        x.append(x[-1])
        if i[0] == 'addx':
            x.append(x[-1] + int(i[1]))
    print(sum(n * x[n-1] for n in range(20, 240, 40)))

##########
# part 2 #
##########
    pixels = ['.'] * 240
    for c in range(240):
        if (c % 40) in [x[c]-1, x[c], x[c]+1]:
            pixels[c] = '#'
    for n in range (0, 240, 40):
        print(''.join(pixels[n:n + 40]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
