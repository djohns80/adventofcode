import argparse
import os

def surface_area(dims):
    return (2 * (dims[0] * dims[1])) + (2 * (dims[0] * dims[2])) + (2 * (dims[1] * dims[2]))

def volume(dims):
    return dims[0] * dims[1] * dims[2]

def area_smmallest_side(dims):
    sort_dim = sorted(dims)
    return sort_dim[0] * sort_dim[1]

def smmallest_circumference(dims):
    sort_dim = sorted(dims)
    return (2 * sort_dim[0]) + (2 * sort_dim[1])

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    dimensions = file.read().strip().split('\n')
    dimensions = [[int(l) for l in d.split('x')] for d in dimensions]

##########
# part 1 #
##########
    sqft = [surface_area(d) + area_smmallest_side(d) for d in dimensions]
    print(sum(sqft))

##########
# part 2 #
##########
    ft = [volume(d) + smmallest_circumference(d) for d in dimensions]
    print(sum(ft))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
