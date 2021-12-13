def perform_fold(_coords, axis, coord):
    new_coords = []
    if axis == 'y':
        for n in range(len(_coords)-1,-1,-1):
            if _coords[n][1] > coord:
                old = _coords.pop(n)
                new = (old[0], (coord*2)-old[1])
                new_coords.append(new)
    elif axis == 'x':
        for n in range(len(_coords)-1,-1,-1):
            if _coords[n][0] > coord:
                old = _coords.pop(n)
                new = ((coord*2)-old[0], old[1])
                new_coords.append(new)
    return list(set(_coords + new_coords))

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    data = file.read()
    coords, folds = data.split('\n\n')
    coords = [l.strip().split(',') for l in coords.splitlines()]
    coords = [(int(c[0]),int(c[1])) for c in coords]
    folds = [l.strip()[11:].split('=') for l in folds.splitlines()]

##########
# part 1 #
##########
    f = folds[0]
    coords = perform_fold(coords, f[0], int(f[1]))
    print(len(coords))

##########
# part 2 #
##########
    for f in folds[1:]:
        coords = perform_fold(coords, f[0], int(f[1]))

    for y in range(max([y for x,y in coords])+1):
        print(''.join(['#' if (x,y) in coords else ' ' for x in range(max([x for x,y in coords])+1)]))
