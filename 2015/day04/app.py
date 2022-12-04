import argparse
import os
import hashlib

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    secret_key = file.read().strip()

##########
# part 1 #
##########
    n = 1
    while not hashlib.md5((f'{secret_key}{n}').encode('utf-8')).hexdigest().startswith('0'*5):
        n += 1
    print(n)

##########
# part 2 #
##########
    while not hashlib.md5((f'{secret_key}{n}').encode('utf-8')).hexdigest().startswith('0'*6):
        n += 1
    print(n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
