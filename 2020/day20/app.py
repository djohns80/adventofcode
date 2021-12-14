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
                    return (kt, s)
                if edge[::-1] == st:
                    return (kt, f'{s}-reverse')
    return None

def match_tiles():
    for k in tiles.keys():
        if k != 'master':
            matches = {e: match_edge(k, es) for e, es in get_edges(k).items()}
            tile_matches[k] = matches

def rotate_clockwise(tile_id):
    tiles[tile_id] = [''.join([tiles[tile_id][y][x] for y in range(len(tiles[tile_id])-1,-1,-1)]) for x in range(len(tiles[tile_id][0]))]
    match_tiles()

def rotate_anticlockwise(tile_id):
    tiles[tile_id] = [''.join([tiles[tile_id][y][x] for y in range(len(tiles[tile_id]))]) for x in range(len(tiles[tile_id][0])-1,-1,-1)]
    match_tiles()

def rotate_180(tile_id):
    tiles[tile_id] = [''.join([tiles[tile_id][y][x] for x in range(len(tiles[tile_id][0])-1,-1,-1)]) for y in range(len(tiles[tile_id])-1,-1,-1)]
    match_tiles()

def flip_horizontal(tile_id):
    tiles[tile_id] = [tiles[tile_id][y] for y in range(len(tiles[tile_id])-1,-1,-1)]
    match_tiles()

def flip_vertical(tile_id):
    tiles[tile_id] = [r[::-1] for r in tiles[tile_id]]
    match_tiles()

def flip_diagonal_forward(tile_id):
    tiles[tile_id] = [''.join([tiles[tile_id][y][x] for y in range(len(tiles[tile_id])-1,-1,-1)]) for x in range(len(tiles[tile_id][0])-1,-1,-1)]
    match_tiles()

def flip_diagonal_backward(tile_id):
    tiles[tile_id] = [''.join([tiles[tile_id][y][x] for y in range(len(tiles[tile_id]))]) for x in range(len(tiles[tile_id][0]))]
    match_tiles()

def get_master_image(tile_ids):
    master_lines = []
    for tile_row in tile_ids:
        for y in range(1, len(tiles[tile_row[0]])-1):
            temp = []
            for tid in tile_row:
                temp.append(tiles[tid][y][1:-1])
            master_lines.append(''.join(temp))
    return master_lines

def count_monsters(full_image):
    monster = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    ]
    points = [(x,y) for y,l in enumerate(monster) for x,c in enumerate(l) if c =='#']
    count = 0
    for y, r in enumerate(full_image[:-2]):
        for x in range(len(r)-20):
            if all([full_image[y+my][x+mx] == '#' for mx, my in points]):
                count += 1
    return count * len(points)

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
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
    methods_y = {
        'top': None,
        'top-reverse': 'flip_vertical',
        'right': 'rotate_anticlockwise',
        'right-reverse': 'flip_diagonal_forward',
        'bottom': 'flip_horizontal',
        'bottom-reverse': 'rotate_180',
        'left': 'flip_diagonal_backward',
        'left-reverse': 'rotate_clockwise'
    }
    methods_x = {
        'top': 'flip_diagonal_backward',
        'top-reverse': 'rotate_anticlockwise',
        'right': 'flip_vertical',
        'right-reverse': 'rotate_180',
        'bottom': 'rotate_clockwise',
        'bottom-reverse': 'flip_diagonal_forward',
        'left': None,
        'left-reverse': 'flip_horizontal'
    }

    # Start with arbitrary first corner
    master_grid = [[[k for k, v in tile_matches.items() if len([t for t in v.values() if t is not None]) == 2][0]]]
    # Rotate this starting corner to be in correct orientation (left and top have no match)
    sides = set([k for k,v in tile_matches[master_grid[0][0]].items() if v is not None])
    if sides == {'bottom', 'left'}:
        rotate_anticlockwise(master_grid[0][0])
    elif sides == {'top', 'left'}:
        rotate_180(master_grid[0][0])
    elif sides == {'top', 'right'}:
        rotate_clockwise(master_grid[0][0])
    bottom_match = tile_matches[master_grid[-1][0]]['bottom']
    # Transform each bottom match so that it matches with top
    while bottom_match:
        master_grid.append([bottom_match[0]])
        if methods_y[bottom_match[1]]:
            locals()[methods_y[bottom_match[1]]](bottom_match[0])
        bottom_match = tile_matches[master_grid[-1][0]]['bottom']
    # Go across each row matching right to make left
    for yo in master_grid:
        right_match = tile_matches[yo[0]]['right']
        while right_match:
            yo.append(right_match[0])
            if methods_x[right_match[1]]:
                locals()[methods_x[right_match[1]]](right_match[0])
            right_match = tile_matches[yo[-1]]['right']
    monster_hash_count = 0
    # rotate master grid until monsters found
    for action in [None, 'rotate_clockwise','rotate_anticlockwise','rotate_180','flip_horizontal','flip_vertical','flip_diagonal_forward','flip_diagonal_backward']:
        tiles['master'] = get_master_image(master_grid)
        if action:
            locals()[action]('master')
        monster_hash_count = count_monsters(tiles['master'])
        if monster_hash_count != 0:
            break
    print(len(''.join(tiles['master'])) - len(''.join(tiles['master']).replace('#','')) - monster_hash_count)
