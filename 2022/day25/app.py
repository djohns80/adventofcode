import argparse
import os

s_to_d = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
d_to_s = {0: '0', 1: '1', 2: '2', 3: '=', 4: '-'}

def snafu_decimal(s):
    return sum((5 ** (len(s) - 1 - i) * s_to_d[d]) for i, d in enumerate(s))

def decimal_snafu(n):
    r = ''
    while n > 0:
        n, rem = divmod(n, 5)
        r += d_to_s[rem]
        if rem > 2:
            n += 1
    return r[::-1] if r else '0'

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().splitlines()

##########
# part 1 #
##########
    print(decimal_snafu(sum(snafu_decimal(l) for l in lines)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
