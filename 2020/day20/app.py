import math

def get_edges(tile_id):
    tile = tiles[tile_id]
    return {
        'top': tile[0],
        'right': ''.join([l[-1] for l in tile]),
        'bottom': tile[-1],
        'left': ''.join([l[0] for l in tile])
    }

def match_edge(tile_id, edge):
    for kt in tiles.keys():
        if kt != tile_id:
            for s, st in get_edges(kt).items():
                if edge == st:
                    return (kt, s, True)
                if edge[::-1] == st:
                    return (kt, s, False)
    return None

def match_tiles():
    for k in tiles.keys():
        matches = {e: match_edge(k, es) for e, es in get_edges(k).items()}
        tile_matches[k] = matches

def rotate_clockwise(tile_id):
    tiles[tile_id] = [''.join([tiles[tile_id][y][x] for y in range(len(tiles[tile_id])-1,-1,-1)]) for x in range(len(tiles[tile_id][0]))]
    match_tiles()

def flip_horizontal(tile_id):
    tiles[tile_id] = [tiles[tile_id][y] for y in range(len(tiles[tile_id])-1,-1,-1)]
    match_tiles()

def flip_vertical(tile_id):
    tiles[tile_id] = [r[::-1] for r in tiles[tile_id]]
    match_tiles()

def print_tile(tile_id):
    for r in tiles[tile_id]:
        print(r)

if __name__ == '__main__':
    file = open('sample', 'r')
#    file = open('input', 'r')
    lines = file.read()
    tiles = {int(tile.splitlines()[0][:-1].split()[1]): tile.splitlines()[1:] for tile in lines.split('\n\n')}
    tile_matches = {}
    match_tiles()

##########
# part 1 #
##########
    print(math.prod([k for k, v in tile_matches.items() if len([t for t in v.values() if t is not None]) == 2]))

##########
# part 2 #
##########
    print([k for k, v in tile_matches.items() if len([t for t in v.values() if t is not None]) == 2][0])

    rotate_clockwise(1951)
    print(tile_matches[1951])
    rotate_clockwise(2729)
    print(tile_matches[2729])
    rotate_clockwise(2971)
    print(tile_matches[2971])
