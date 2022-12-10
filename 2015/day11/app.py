import argparse
import os

def incr_chr(c):
    return chr(ord(c) + 1) if c != 'z' else 'a'

def incr_str(s):
    lpart = s.rstrip('z')
    num_replacements = len(s) - len(lpart)
    new_s = lpart[:-1] + incr_chr(lpart[-1]) if lpart else 'a'
    new_s += 'a' * num_replacements
    return new_s

def allowed_chrs(p):
    return not any([c in p for c in ['i','o', 'l']])

def chr_sequence(p):
    ords = list(map(ord, list(p)))
    for n, o in enumerate(ords[2:]):
        if ords[n] == o - 2 and ords[n+1] == o - 1:
            return True
    return False

def two_pairs(p):
    chars = list('abcdefghjkmnpqrstuvwxyz')
    pairs = [''.join(p) for p in zip(chars, chars)]
    return sum([int(c in p) for c in pairs]) >= 2

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = file.read().strip()

##########
# part 1 #
##########
    while len(data) == 8:
        data = incr_str(data)
        if allowed_chrs(data) and chr_sequence(data) and two_pairs(data):
            break
    print(data)

##########
# part 2 #
##########
    while len(data) == 8:
        data = incr_str(data)
        if allowed_chrs(data) and chr_sequence(data) and two_pairs(data):
            break
    print(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
