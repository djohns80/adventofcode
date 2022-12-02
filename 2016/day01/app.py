from collections import defaultdict

if __name__ == '__main__':
    file = open('input', 'r', encoding='utf-8')
    steps = [(d[0], int(d[1:])) for d in file.read().strip().split(', ')]

    direction = 0 + 1j
    position = 0 + 0j
    positions = defaultdict(int)
    positions[position] += 1
    part2 = None
    for s in steps:
        if s[0] == 'L':
            direction *= 1j
        elif s[0] == 'R':
            direction *= -1j
        for n in range(s[1]):
            position += direction
            positions[position] += 1
            if positions[position] > 1 and part2 is None:
                part2 = int(abs(position.real) + abs(position.imag))
    part1 = int(abs(position.real) + abs(position.imag))

##########
# part 1 #
##########
    print(part1)

##########
# part 2 #
##########
    print(part2)
