import argparse
import os

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    data = [int(d) for d in file.read().strip().split(',')]

##########
# part 1 #
##########
    data1 = data.copy()
    input = 1
    output = 0
    n = 0
    while n < len(data1):
        code_list = list(f'{data1[n]:05}')
        op_code = int(''.join(code_list[3:5]))
        modes = {
            1: int(code_list[2]),
            2: int(code_list[1]),
            3: int(code_list[0])
        }
        if op_code == 1:
            param1 = data1[n+1] if modes[1] == 1 else data1[data[n+1]]
            param2 = data1[n+2] if modes[2] == 1 else data1[data[n+2]]
            data1[data1[n+3]] = param1 + param2
            n += 4
        elif op_code == 2:
            param1 = data1[n+1] if modes[1] == 1 else data1[data1[n+1]]
            param2 = data1[n+2] if modes[2] == 1 else data1[data1[n+2]]
            data1[data1[n+3]] = param1 * param2
            n += 4
        elif op_code == 3:
            data1[data1[n+1]] = input
            n += 2
        elif op_code == 4:
            output = data1[data1[n+1]]
            n += 2
        elif op_code == 99:
            break
    print(output)

##########
# part 2 #
##########
    data2 = data.copy()
    input = 5
    output = 0
    n = 0
    while n < len(data2):
        code_list = list(f'{data2[n]:05}')
        op_code = int(''.join(code_list[3:5]))
        modes = {
            1: int(code_list[2]),
            2: int(code_list[1]),
            3: int(code_list[0])
        }
        if op_code == 1:
            param1 = data2[n+1] if modes[1] == 1 else data2[data[n+1]]
            param2 = data2[n+2] if modes[2] == 1 else data2[data[n+2]]
            data2[data2[n+3]] = param1 + param2
            n += 4
        elif op_code == 2:
            param1 = data2[n+1] if modes[1] == 1 else data2[data2[n+1]]
            param2 = data2[n+2] if modes[2] == 1 else data2[data2[n+2]]
            data2[data2[n+3]] = param1 * param2
            n += 4
        elif op_code == 3:
            data2[data2[n+1]] = input
            n += 2
        elif op_code == 4:
            output = data2[data2[n+1]]
            n += 2
        elif op_code == 5:
            param1 = data2[n+1] if modes[1] == 1 else data2[data[n+1]]
            param2 = data2[n+2] if modes[2] == 1 else data2[data[n+2]]
            if param1 != 0:
                n = param2
            else:
                n += 3
        elif op_code == 6:
            param1 = data2[n+1] if modes[1] == 1 else data2[data[n+1]]
            param2 = data2[n+2] if modes[2] == 1 else data2[data[n+2]]
            if param1 == 0:
                n = param2
            else:
                n += 3
        elif op_code == 7:
            param1 = data2[n+1] if modes[1] == 1 else data2[data[n+1]]
            param2 = data2[n+2] if modes[2] == 1 else data2[data[n+2]]
            data2[data2[n+3]] = 1 if param1 < param2 else 0
            n += 4
        elif op_code == 8:
            param1 = data2[n+1] if modes[1] == 1 else data2[data[n+1]]
            param2 = data2[n+2] if modes[2] == 1 else data2[data[n+2]]
            data2[data2[n+3]] = 1 if param1 == param2 else 0
            n += 4
        elif op_code == 99:
            break
    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
