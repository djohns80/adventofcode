from collections import Counter

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [int(l.strip()) for l in lines]

##########
# part 1 #
##########
    lines.append(0)
    lines.append(max(lines)+3)
    lines.sort()
    diffs = [lines[i] - lines[i - 1] for i in range(1, len(lines))]
    counts = dict(Counter(diffs))
    print(counts[1] * counts[3])

###########
## part 1 #
###########
    sol = {0:1}
    for line in lines[1:]:
        sol[line] = 0
        if line - 1 in sol:
            sol[line] += sol[line-1]
        if line - 2 in sol:
            sol[line] += sol[line-2]
        if line - 3 in sol:
            sol[line] += sol[line-3]
    print(sol[max(lines)])