if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [int(l.strip()) for l in lines]

##########
# part 1 #
##########
    preamble_length = 25
    invalid_number = None
    for n in range(preamble_length,len(lines)):
        preamble = lines[n-preamble_length:n]
        sums = [v1 + v2 for v1i, v1 in enumerate(preamble) for v2i, v2 in enumerate(preamble) if v2i > v1i]
        if lines[n] not in sums:
            invalid_number = lines[n]
            break
    print(invalid_number)

##########
# part 2 #
##########
    for n, v in enumerate(lines):
        sum = v
        i = 1
        while sum < invalid_number:
            sum += lines[n+i]
            i += 1
        if sum == invalid_number:
            sorted_set = sorted(lines[n:n+i])
            print(min(sorted_set) + max(sorted_set))
            break
