import argparse
import os
import sys
import functools

def compare(left, right):
    match left, right:
        case int(), int():
            return left - right
        case list(), list():
            for l, r in zip(left, right):
                if diff := compare(l, r):
                    return diff
            return len(left) - len(right)
        case int(), list():
            return compare([left], right)
        case list(), int():
            return compare(left, [right])

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().splitlines()

##########
# part 1 #
##########
    packet_pairs = [{'l': eval(lines[n]), 'r': eval(lines[n + 1])} for n in range(0, len(lines), 3)]
    print(sum(n + 1 for n, p in enumerate(packet_pairs) if compare(p['l'], p['r']) < 0))

##########
# part 2 #
##########
    packets = [eval(l) for l in lines if l]
    packets.append([[2]])
    packets.append([[6]])
    sorted_packets = sorted(packets, key=functools.cmp_to_key(compare))
    print((sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1))

if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
