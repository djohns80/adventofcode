import argparse
import os
import itertools

def intcode_program(data, inputs):
    outputs = []
    n = 0
    while n < len(data):
        code_list = list(f'{data[n]:05}')
        op_code = int(''.join(code_list[3:5]))
        modes = {
            1: int(code_list[2]),
            2: int(code_list[1]),
            3: int(code_list[0])
        }
        if op_code == 1:
            param1 = data[n+1] if modes[1] == 1 else data[data[n+1]]
            param2 = data[n+2] if modes[2] == 1 else data[data[n+2]]
            data[data[n+3]] = param1 + param2
            n += 4
        elif op_code == 2:
            param1 = data[n+1] if modes[1] == 1 else data[data[n+1]]
            param2 = data[n+2] if modes[2] == 1 else data[data[n+2]]
            data[data[n+3]] = param1 * param2
            n += 4
        elif op_code == 3:
            data[data[n+1]] = inputs[0]
            inputs = inputs[1:]
            n += 2
        elif op_code == 4:
            outputs.append(data[data[n+1]])
            n += 2
        elif op_code == 5:
            param1 = data[n+1] if modes[1] == 1 else data[data[n+1]]
            param2 = data[n+2] if modes[2] == 1 else data[data[n+2]]
            if param1 != 0:
                n = param2
            else:
                n += 3
        elif op_code == 6:
            param1 = data[n+1] if modes[1] == 1 else data[data[n+1]]
            param2 = data[n+2] if modes[2] == 1 else data[data[n+2]]
            if param1 == 0:
                n = param2
            else:
                n += 3
        elif op_code == 7:
            param1 = data[n+1] if modes[1] == 1 else data[data[n+1]]
            param2 = data[n+2] if modes[2] == 1 else data[data[n+2]]
            data[data[n+3]] = 1 if param1 < param2 else 0
            n += 4
        elif op_code == 8:
            param1 = data[n+1] if modes[1] == 1 else data[data[n+1]]
            param2 = data[n+2] if modes[2] == 1 else data[data[n+2]]
            data[data[n+3]] = 1 if param1 == param2 else 0
            n += 4
        elif op_code == 99:
            break
    return outputs


def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    software = [int(d) for d in file.read().strip().split(',')]

##########
# part 1 #
##########
#    thruster_signals = {}
#    for ps in itertools.permutations(range(5)):
#        input_signal = 0
#        for s in ps:
#            input_signal = intcode_program(software.copy(), [s, input_signal])[0]
#        thruster_signals[ps] = input_signal
#    print(max(thruster_signals.values()))

##########
# part 2 #
##########
#    ### TODO: complete part 2
#    input_signal = 0
#    for s in [9,8,7,6,5]:
#        input_signal = intcode_program(software.copy(), [s, input_signal])[0]
#    print(input_signal)

    print(intcode_program(software.copy(), [9, 0]))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='sample')
    args = parser.parse_args()
    main(args.input)
