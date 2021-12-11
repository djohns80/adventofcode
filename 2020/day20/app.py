import math

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.read()
    tiles = {int(tile.splitlines()[0][:-1].split()[1]): tile.splitlines()[1:] for tile in lines.split('\n\n')}

##########
# part 1 #
##########
    edges = {}
    for id, tile_lines in tiles.items():
        edges[id] = [
            tile_lines[0],
            ''.join([l[-1] for l in tile_lines]),
            tile_lines[-1],
            ''.join([l[0] for l in tile_lines])
        ]
    tile_types = {}
    for k, v in edges.items():
        others = [st for kt, vt in edges.items() for st in vt if kt != k]
        matches = [s in others or s[::-1] in others for s in v]
        tile_types[k] = sum(matches)
    print(math.prod([k for k, v in tile_types.items() if v == 2])) #605

##########
# part 2 #
##########
