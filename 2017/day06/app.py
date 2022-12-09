import argparse
import os
import itertools

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    banks = list(map(int, file.read().strip().split()))

##########
# part 1 #
##########

    seen = {}
    count = 0
    while tuple(banks) not in seen:
        seen[tuple(banks)] = count
        max_index, max_value = max(enumerate(banks), key=lambda k: (k[1], -k[0]))
        banks[max_index] = 0
        for i in itertools.islice(itertools.cycle(range(len(banks))), max_index + 1, max_index + max_value + 1):
            banks[i] += 1
        count += 1
    print(count)

##########
# part 2 #
##########
    print(count - seen[tuple(banks)])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
