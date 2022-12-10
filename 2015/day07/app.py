import argparse
import os
import re

def get_value(wires, v):
    try:
        v = int(v, 10)
    except (ValueError, TypeError):
        pass
    return v if isinstance(v, int) else wires[v]

def run_program(wires, instructions):
    while len(wires) != len(instructions):
        for i in instructions:
            if i['out'] not in wires:
                try:
                    match i['operator']:
                        case None:
                            wires[i['out']] = get_value(wires, i['in1'])
                        case 'AND':
                            wires[i['out']] = get_value(wires, i['in1']) & get_value(wires, i['in2'])
                        case 'OR':
                            wires[i['out']] = get_value(wires, i['in1']) | get_value(wires, i['in2'])
                        case 'NOT':
                            wires[i['out']] = ~get_value(wires, i['in2']) & 65535
                        case 'LSHIFT':
                            wires[i['out']] = get_value(wires, i['in1']) << get_value(wires, i['in2'])
                        case 'RSHIFT':
                            wires[i['out']] = get_value(wires, i['in1']) >> get_value(wires, i['in2'])
                except KeyError:
                    pass
    return wires

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = [m.groupdict() for m in re.finditer(r'(?:(?P<in1>[a-z]+|\d+)\s)?(?:(?P<operator>AND|OR|NOT|LSHIFT|RSHIFT)\s)?(?:(?P<in2>[a-z]+|\d+)\s)?->\s(?P<out>[a-z]+|\d+)', file.read())]

##########
# part 1 #
##########
    part1 = run_program({}, data)
    print(part1['a'])

##########
# part 2 #
##########
    part2 = run_program({'b': part1['a']}, data)
    print(part2['a'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
