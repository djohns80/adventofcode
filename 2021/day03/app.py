def separate_numbers(numbers, position):
    separated = {}
    for number in numbers:
        char = number[position]
        if char in separated:
            separated[char].append(number)
        else:
            separated[char] = [number]
    return separated

def check_common(numbers, position, check):
    separated = separate_numbers(numbers, position)
    if len(separated['0']) == len(separated['1']):
        if check == 'most':
            result = '1'
        elif check == 'least':
            result = '0'
    else:
        if check == 'most':
            result = str(int(len(separated['0']) < len(separated['1'])))
        elif check == 'least':
            result = str(int(len(separated['0']) > len(separated['1'])))
    return separated[result]

def get_rating(numbers, check):
    i = 0
    temp = numbers
    while len(temp) != 1:
        temp = check_common(temp, i, check)
        i += 1
    return int(temp[0], 2)

if __name__ == '__main__':
    #file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

##########
# part 1 #
##########
    line_count = len(lines)
    common = []
    for line in lines:
        for n, b in enumerate(line):
            if len(common) <= n:
                common.append(int(b))
            else:
                common[n] += int(b)
    gamma = int(''.join([str(int(b > (line_count / 2))) for b in common]), 2)
    epsilon = int(''.join([str(int(not b > (line_count / 2))) for b in common]), 2)
    print(gamma * epsilon)

##########
# part 2 #
##########
    oxygen_generator_rating = get_rating(lines, 'most')
    co2_generator_rating = get_rating(lines, 'least')
    print(oxygen_generator_rating * co2_generator_rating)
