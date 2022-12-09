import argparse
import os

def get_path(planet, orbits, path):
    if orbits[planet] == 'COM':
        return path + '-' + orbits[planet]
    else:
        return get_path(orbits[planet], orbits, path + '-' + orbits[planet])

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    raw_orbits = [l.strip().split(')') for l in file.readlines()]

##########
# part 1 #
##########
    dict_orbits = {r[1]:r[0] for r in raw_orbits}
    assert(len(dict_orbits.keys()) == len(raw_orbits))
    paths = {}
    count_orbits = 0
    for k in dict_orbits.keys():
        paths[k] = get_path(k, dict_orbits, k)
        count_orbits += (len(paths[k]) - len(paths[k].replace('-','')))
    print(count_orbits)

##########
# part 2 #
##########
    for y in paths['YOU'].split('-'):
        if y in paths['SAN'].split('-'):
            break
    print(paths['YOU'].split('-').index(y) + paths['SAN'].split('-').index(y) - 2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
