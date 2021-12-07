if __name__ == '__main__':
    #file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

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
