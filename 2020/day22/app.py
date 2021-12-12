if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.read()
    p1, p2 = lines.split('\n\n')
    p1 = [int(c) for c in p1.splitlines()[1:]]
    p2 = [int(c) for c in p2.splitlines()[1:]]

##########
# part 1 #
##########
    while p1 and p2:
        if p1[0] > p2[0]:
            p1.extend(sorted([p1.pop(0),p2.pop(0)])[::-1])
        else:
            p2.extend(sorted([p1.pop(0),p2.pop(0)])[::-1])
    scores = [abs(n-len(p1+p2)) * v for n, v in enumerate(p1 + p2)]
    print(sum(scores))

##########
# part 2 #
##########
