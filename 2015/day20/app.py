import argparse
import os
import math

def get_divisors(n):
    d = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            d.update((i, int(n / i)))
    return d

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = int(file.read().strip())

    part1 = None
    part2 = None
    i = 0
    while not part1 or not part2:
        i += 1
        divisors = get_divisors(i)
        if not part1:
            if sum(divisors) * 10 >= data:
                part1 = i
        if not part2:
            if sum(d for d in divisors if i / d <= 50) * 11 >= data:
                part2 = i

##########
# part 1 #
##########
    print(part1)

##########
# part 2 #
##########
    print(part2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
