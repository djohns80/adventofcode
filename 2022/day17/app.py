import argparse
import os
import itertools
from collections import defaultdict
def translatex(rock, dx):
    for i in range(len(rock)):
        rock[i][0] += dx

def translatey(rock, dy):
    for i in range(len(rock)):
        rock[i][1] += dy

def checkwalls(rock, dx):
    for p in rock:
        if not (0 <= p[0]+dx <= 6):
            return False
    return True

def checkblock(rock, c, dx, dy):
    for x, y in rock:
        if (x + dx, y + dy) in c:
            return False
    return True

def prune(c, top):
    for p in [p for p in c if p[1] < top - 50]:
        c.remove(p)

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = file.read().strip()
    jets = itertools.cycle(data)
    jetdir = {'<': -1, '>': 1}
    rocks = itertools.cycle((
        ((0, 0), (1, 0), (2, 0), (3, 0)),
        ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
        ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
    ))
    col = set([(x, 0) for x in range(7)])

##########
# part 1 #
##########
    target = 1_000_000_000_000 - 1
    top = 0
    n = -1
    tracker = defaultdict(list)
    initial = None
    divisor = None
    amount = None
    tgtidx = -1

    while True:
        n += 1
        rock = [[x + 2, y + top + 4] for x, y in next(rocks)]
        while True:
            dir = jetdir[next(jets)]
            if checkwalls(rock, dir) and checkblock(rock, col, dir, 0):
                translatex(rock, dir)
            if not checkblock(rock, col, 0, -1):
                break
            translatey(rock, -1)
        col.update([(x, y) for x, y in rock])
        top = max([p[1] for p in rock] + [top])
        prune(col, top)

        if n == 2021:
            print(top)

##########
# part 2 #
##########
        if n == tgtidx:
            modulus = top - (initial + ((n // divisor) - 1) * amount)
            part2 = initial + ((target // divisor) - 1) * amount + modulus
            print(part2)
            break

        # skip tracking after finding divisor
        if divisor is not None:
            continue

        # track differences for divisors and return the first one that is the same for 3 times in a row
        if n != 0:
            tracker[n] = [(top, top)]

        for i in [i for i in tracker if n % i == 0]:
            tracker[i].append((top, top-tracker[i][-1][0]))
            if len(tracker[i]) > 3 and tracker[i][-1][1] == tracker[i][-2][1] == tracker[i][-3][1] == tracker[i][-4][1]:
                # divisor is how many shapes are required to have a perfect cycle
                divisor = i
                # initial is the height for the first cycle since it's different
                initial = tracker[i][0][0]
                # amount is the height per normal cycle
                amount = tracker[i][-1][1]
                # run for modulus more cycles
                tgtidx = n + (target % divisor)
                # delete tracker
                tracker = None
                break
            elif len(tracker[i]) > 3 and tracker[i][-1][1] != tracker[i][-2][1]:
                del tracker[i]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
