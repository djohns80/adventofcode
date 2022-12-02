from collections import defaultdict

if __name__ == '__main__':
    file = open('input', 'r', encoding='utf-8')
    changes = [int(c) for c in file.read().split('\n') if c != '']

##########
# part 1 #
##########
    print(sum(changes))

##########
# part 2 #
##########
    frequencies = defaultdict(int)
    current_frequency = 0
    frequencies[current_frequency] += 1
    while True:
        for c in changes:
            current_frequency += c
            frequencies[current_frequency] += 1
            if frequencies[current_frequency] > 1:
                break
        if frequencies[current_frequency] > 1:
            break
    print(current_frequency)
