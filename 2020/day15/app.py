import re

if __name__ == '__main__':
#    input = '0,3,6'
    input = '5,2,8,16,18,0,1'
    numbers = input.split(',')

    turn = None
    last_spoken = None
    numbers_spoken = {}
##########
# part 1 #
##########
#    turns = 2020
##########
# part 2 #
##########
    turns = 30000000

    for i, n in enumerate(numbers):
        last_spoken = int(n)
        if last_spoken in numbers_spoken:
            numbers_spoken[last_spoken] = (numbers_spoken[last_spoken][1], i + 1)
        else:
            numbers_spoken[last_spoken] = (0, i + 1)
    turn = len(numbers) + 1
    while turn <= turns:
        if numbers_spoken[last_spoken] == (0,turn - 1):
            last_spoken = 0
        else:
            last_spoken = numbers_spoken[last_spoken][1] - numbers_spoken[last_spoken][0]
        if last_spoken in numbers_spoken:
            numbers_spoken[last_spoken] = (numbers_spoken[last_spoken][1], turn)
        else:
            numbers_spoken[last_spoken] = (0, turn)
        turn += 1
    print(last_spoken)

