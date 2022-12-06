import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    datastream = file.read().strip()

##########
# part 1 #
##########
    for i in range(3,len(datastream)):
        if len(set(datastream[i-3:i+1])) == 4:
            break
    print(i+1)

##########
# part 2 #
##########
    for i in range(13,len(datastream)):
        if len(set(datastream[i-13:i+1])) == 14:
            break
    print(i+1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
