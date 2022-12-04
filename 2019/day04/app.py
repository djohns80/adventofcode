import argparse
import os
from collections import Counter

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    pwd_rng = [int(v) for v in file.read().strip().split('-')]

##########
# part 1 #
##########
    valid_pwds = []
    for v in range(pwd_rng[0], pwd_rng[1]):
        digits = [int(d) for d in list(str(v))]
        six_digits = len(digits) == 6
        increasing = all(i <= j for i, j in zip(digits, digits[1:]))
        doubles = any(i == j for i, j in zip(digits, digits[1:]))
        if all([six_digits, doubles, increasing]):
            valid_pwds.append(v)
    print(len(valid_pwds))

##########
# part 2 #
##########
    new_valid_pwds = [p for p in valid_pwds if 2 in Counter(list(str(p))).values()]
    print(len(new_valid_pwds))

if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
