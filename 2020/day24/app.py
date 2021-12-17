if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

    dirs = {
        'e': (1, -1, 0),
        'se': (0, -1, 1),
        'sw': (-1, 0, 1),
        'w': (-1, 1, 0),
        'nw': (0, 1, -1),
        'ne': (1, 0, -1)
    }

    paths = []
    for l in lines:
        path = []
        chars = list(l)
        while chars:
            c = chars.pop(0)
            if c in ['n','s']:
                path.append(c + chars.pop(0))
            else:
                path.append(c)
        paths.append(path)

##########
# part 1 #
##########
    black_tiles = set()
    for path in paths:
        tile = (0, 0, 0)
        for p in path:
            tile = tuple([a + b for a, b in zip(tile, dirs[p])])
        if tile in black_tiles:
            black_tiles.remove(tile)
        else:
            black_tiles.add(tile)
    print(len(black_tiles))

##########
# part 2 #
##########
    for _ in range(100):
        new_tiles = set()
        check_tiles = set()
        for tile in black_tiles:
            check_tiles.add(tile)
            for diff in dirs.values():
                check_tiles.add(tuple([a + b for a, b in zip(tile, diff)]))
        for tile in check_tiles:
            neighbour_count = sum([tuple(a + b for a, b in zip(tile, d)) in black_tiles for d in dirs.values()])
            if (tile in black_tiles and 0 < neighbour_count <= 2) or (tile not in black_tiles and neighbour_count == 2):
                new_tiles.add(tile)
        black_tiles = new_tiles
    print(len(black_tiles))
