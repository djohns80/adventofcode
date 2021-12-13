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

def print_tile(tile_ids):
    for r in range(len(tiles[tile_ids[0]])):
        line = []
        for tid in tile_ids:
            line.append(tiles[tid][r][None:None])
        print('|'.join(line))

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
    monster = [(18,0),(0,1),(5,1),(6,1),(11,1),(12,1),(17,1),(18,1),(19,1),(1,2),(4,2),(7,2),(10,2),(13,2),(16,2)]
    count = 0
    for y, r in enumerate(full_image[:-2]):
        for x in range(len(r)-20):
            if all([full_image[y+my][x+mx] == '#' for mx, my in monster]):
                count += 1
    return count * len(monster)

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
    methods = {
        'top': 'flip_diagonal_backward',
        'top-reverse': 'rotate_anticlockwise',
        'right': 'flip_vertical',
        'right-reverse': 'rotate_180',
        'bottom': 'rotate_clockwise',
        'bottom-reverse': 'flip_diagonal_forward',
        'left': None,
        'left-reverse': 'flip_horizontal'
    }
#    master_grid = [
#        [1753, 2693, 1583, 3559, 3851, 2473, 2689, 2879, 2503, 2351, 1579, 2843],
#        [1609, 2393, 1123, 2003, 1543, 2857, 2797, 1117, 2161, 3739, 3823, 2549],
#    ]
    flip_vertical(1609)
    flip_horizontal(1559)
    flip_diagonal_forward(1297)
    flip_horizontal(2153)
    rotate_clockwise(2447)
    rotate_180(1069)
    flip_vertical(1483)
    rotate_anticlockwise(1031)
    rotate_180(1787)
    flip_vertical(1489)

    master_grid = [
        [1753],
        [1609],
        [1559],
        [1297],
        [3793],
        [2153],
        [2447],
        [1069],
        [1483],
        [1031],
        [1787],
        [1489]
    ]
    for yo in master_grid:
        for co in range(11):
            right_match = tile_matches[yo[co]]['right']
            if methods[right_match[1]]:
                locals()[methods[right_match[1]]](right_match[0])
            yo.append(right_match[0])

    tiles['master'] = get_master_image(master_grid)
#    rotate_clockwise('master')
#    rotate_anticlockwise('master')
#    rotate_180('master')
#    flip_horizontal('master')
#    flip_vertical('master')
#    flip_diagonal_forward('master')
    flip_diagonal_backward('master')
    monster_hash_count = count_monsters(tiles['master'])
    print(len(''.join(tiles['master'])) - len(''.join(tiles['master']).replace('#','')) - monster_hash_count)


##1951    2729    2971
##2311    1427    1489
##3079    2473    1171
#    rotate_clockwise(1951)
#    rotate_clockwise(2729)
#    rotate_clockwise(2971)
#    rotate_clockwise(2311)
#    rotate_clockwise(1427)
#    rotate_clockwise(1489)
#    flip_diagonal_backward(3079)
#    rotate_180(2473)
#    rotate_anticlockwise(1171)
#
#    master_image = get_master_image([[1951,2729,2971],[2311,1427,1489],[3079,2473,1171]])
#    monster_hash_count = count_monsters(master_image)
#    print(len(''.join(master_image)) - len(''.join(master_image).replace('#','')) - monster_hash_count)
