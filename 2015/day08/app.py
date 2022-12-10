import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().strip().split('\n')

##########
# part 1 #
##########
    print(sum(len(l) - (len(l.encode('utf-8').decode('unicode_escape')) - 2) for l in lines))

##########
# part 2 #
##########
    print(sum((len(l.replace('\\','\\\\').replace('"','\\"')) + 2) - len(l) for l in lines))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
