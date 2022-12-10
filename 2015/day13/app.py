import argparse
import os
import itertools

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = [l.split() for l in file.read().strip().split('\n')]
    data = {f"{l[0]}-{l[-1].strip('.')}": (1 if l[2] == 'gain' else -1) * int(l[3]) for l in lines}
    people = set([d.split('-')[0] for d in data])

##########
# part 1 #
##########
    print(max(sum(data[f'{a[n-1]}-{a[n-2]}'] + data[f'{a[n-1]}-{p}'] for n, p in enumerate(a)) for a in itertools.permutations(people)))

##########
# part 2 #
##########
    for p in people:
        data[f'Me-{p}'] = 0
        data[f'{p}-Me'] = 0
    people.add('Me')
    print(max(sum(data[f'{a[n-1]}-{a[n-2]}'] + data[f'{a[n-1]}-{p}'] for n, p in enumerate(a)) for a in itertools.permutations(people)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
