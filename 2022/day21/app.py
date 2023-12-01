import argparse
import os
from sympy.solvers import solve

def unwind(m, n):
    monkey = m[n]
    if isinstance(monkey, list):
        expr = unwind(m, monkey[0]), monkey[1], unwind(m, monkey[2])
        return f"({expr[0]} {expr[1]} {expr[2]})"
    return monkey

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    monkeys = {}
    for line in file.read().splitlines():
        name, value = map(str.strip, line.split(':'))
        monkeys[name] = int(value) if value[0].isdigit() else value.split()

##########
# part 1 #
##########
    print(int(eval(unwind(monkeys, 'root'))))

##########
# part 2 #
##########
    monkeys['root'][1] = '-' # Will sove for expression equals 0
    monkeys['humn'] = 'x'
    print(solve(unwind(monkeys, 'root'))[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
