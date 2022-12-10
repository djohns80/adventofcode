import argparse
import os

def look_say(number):
    counts = []
    c = 1
    for n, d in enumerate(number):
        if n == len(number) - 1:
            counts.append((d, c))
        elif d != number[n+1]:
            counts.append((d, c))
            c = 1
        else:
            c += 1
    return ''.join(str(c[1]) + c[0] for c in counts)

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = file.read().strip()

##########
# part 1 #
##########
    for n in range(50):
        data = look_say(data)
        if n == 39:
            print(len(data))

##########
# part 2 #
##########
    print(len(data))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
