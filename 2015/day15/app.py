import argparse
import os
import math

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().strip().split('\n')
    ingredients = {}
    for l in lines:
        name, props = l.split(': ')
        props = props.split(', ')
        props = {p.split()[0]: int(p.split()[1]) for p in props}
        ingredients[name] = props

##########
# part 1 #
##########
    results = {}
    # This loop is hardcoded to 4 ingredients...
    for q in [(s1, s2, s3, 100 - s1 - s2 - s3) for s1 in range(101) for s2 in range(101 - s1) for s3 in range(101 - s1 - s2)]:
        props = [sum(i[p] * q[n] for n, i in enumerate(ingredients.values())) for p in list(ingredients.values())[0]]
        if all(p > 0 for p in props[:len(props) - 1]):
            results[q] = (math.prod(props[:len(props) - 1]), props[-1])
    print(max(r[0] for r in results.values()))

##########
# part 2 #
##########
    print(max(r[0] for r in results.values() if r[1] == 500))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
