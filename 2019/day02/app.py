import argparse
import os

def program(noun, verb):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input'), 'r', encoding='utf-8')
    data = [int(d) for d in file.read().strip().split(',')]

    data[1] = noun
    data[2] = verb
    n = 0
    while n < len(data):
        if data[n] == 1:
            data[data[n+3]] = data[data[n+1]] + data[data[n+2]]
        elif data[n] == 2:
            data[data[n+3]] = data[data[n+1]] * data[data[n+2]]
        elif data[n] == 99:
            break
        n += 4
    return data[0]

def main():
##########
# part 1 #
##########
    print(program(12, 2))

##########
# part 2 #
##########
    for opts in [(n,v) for n in range(100) for v in range(100)]:
        if program(opts[0], opts[1]) == 19690720:
            break
    print((100 * opts[0]) + opts[1])

if __name__ == '__main__':
    main()
