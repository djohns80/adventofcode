import argparse
import os

def swap(l, e):
    i = l.index(e)
    val, _ = l.pop(i)
    iNew = (i+val)%len(l)
    if iNew == 0:
        l.append(e)
        return
    l.insert(iNew, e)    

def mix(l, times = 1):
    new = []
    for i, n in enumerate(l):
        new.append((n, i))
    for _ in range(times):
        for i, n in enumerate(l):
            swap(new, (n, i))
    return list(map(lambda x:x[0], new))

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = list(map(int, file.read().splitlines()))

##########
# part 1 #
##########
    mixed = mix(data)
    s = sum(mixed[(i + mixed.index(0)) % len(mixed)] for i in (1000, 2000, 3000))
    print(s)

##########
# part 2 #
##########
    key = 811589153
    l = list(map(lambda x: x * key, data))
    mixed = mix(l, 10)
    s = sum(mixed[(i + mixed.index(0)) % len(mixed)] for i in (1000, 2000, 3000))
    print(s)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
