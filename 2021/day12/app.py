from collections import defaultdict

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

    caves = defaultdict(list)
    for line in lines:
        a, b = line.split('-')
        if b != 'start' and a != 'end':
            caves[a].append(b)
        if a != 'start' and b != 'end':
            caves[b].append(a)

##########
# part 1 #
##########
    temp = ([('start', {'start'})])
    paths = 0
    while temp:
        node, visited = temp.pop()
        if node != 'end':
            for n in caves[node]:
                if not(n in visited and n.islower()):
                    temp.append((n, visited | {n}))
        else:
            paths += 1
    print(paths)

##########
# part 2 #
##########
    temp = ([('start', {'start'}, False)])
    paths = 0
    while temp:
        node, visited, once = temp.pop()
        if node != 'end':
            for n in caves[node]:
                if not(n in visited and n.islower()):
                    temp.append((n, visited | {n}, once))
                    continue
                if once:
                    continue
                temp.append((n, visited, True))
        else:
            paths += 1
    print(paths)
