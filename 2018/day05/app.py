import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    polymer = file.read().strip()

##########
# part 1 #
##########
    polymer1 = polymer
    a_z = [chr(l + 97) for l in range(26)]
    list1 = [i + j.upper() for i, j in zip(a_z, a_z)]
    list2 = [i.upper() + j for i, j in zip(a_z, a_z)]
    while True:
        before = len(polymer1)
        for r in (list1 + list2):
            polymer1 = polymer1.replace(r, '')
        if len(polymer1) == before:
            break
    print(len(polymer1))

##########
# part 2 #
##########
    results = {}
    for l in a_z:
        polymer2 = polymer.replace(l,'').replace(l.upper(),'')
        while True:
            before = len(polymer2)
            for r in (list1 + list2):
                polymer2 = polymer2.replace(r, '')
            if len(polymer2) == before:
                break
        results[l] = len(polymer2)
    print(min(list(results.values())))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
