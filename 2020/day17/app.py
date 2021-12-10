import copy

def get_neighbors_1(c):
    return [(c[0]+z, c[1]+y, c[2]+x) for z in range(-1, 2) for y in range(-1, 2) for x in range(-1, 2) if not (z == 0 and y == 0 and x == 0)]

def get_neighbors_2(c):
    return [(c[0]+w, c[1]+z, c[2]+y, c[3]+x) for w in range(-1, 2)  for z in range(-1, 2) for y in range(-1, 2) for x in range(-1, 2) if not (w == 0 and z == 0 and y == 0 and x == 0)]

def check_neighbors_1(c, cubes):
    n = get_neighbors_1(c)
    neighbors_count = len([x for x in n if cubes.get(x) == '#'])
    return neighbors_count

def check_neighbors_2(c, cubes):
    n = get_neighbors_2(c)
    neighbors_count = len([x for x in n if cubes.get(x) == '#'])
    return neighbors_count

def cycle_1(cubes):
    new_cube = {}
    for c in cubes:
        x = check_neighbors_1(c, cubes)
        if cubes[c] == '#':
            if x == 2 or x == 3:
                new_cube[c] = '#'
            else:
                new_cube[c] = '.'
            n = get_neighbors_1(c)
            for x in n:
                if x not in cubes:
                    k = check_neighbors_1(x, cubes)
                    if k == 3:
                        new_cube[x] = '#'
        elif cubes[c] == '.':
            if x == 3:
                new_cube[c] = '#'
            else:
                new_cube[c] = '.'
    return new_cube

def cycle_2(cubes):
    new_cube = {}
    for c in cubes:
        x = check_neighbors_2(c, cubes)
        if cubes[c] == '#':
            if x == 2 or x == 3:
                new_cube[c] = '#'
            else:
                new_cube[c] = '.'
            n = get_neighbors_2(c)
            for x in n:
                if x not in cubes:
                    k = check_neighbors_2(x, cubes)
                    if k == 3:
                        new_cube[x] = '#'
        elif cubes[c] == '.':
            if x == 3:
                new_cube[c] = '#'
            else:
                new_cube[c] = '.'
    return new_cube

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines if l.strip() != '']

##########
# part 1 #
##########
    cubes = {(0, y, x):lines[y][x] for y in range(len(lines)) for x in range(len(lines[0]))}
    for i in range(6):
        cubes = cycle_1(cubes)
    print(sum([1 for c in cubes.values() if c == '#']))

##########
# part 2 #
##########
    cubes = {(0, 0, y, x):lines[y][x] for y in range(len(lines)) for x in range(len(lines[0]))}
    for i in range(6):
        cubes = cycle_2(cubes)
    print(sum([1 for c in cubes.values() if c == '#']))
