def get_adjacents(row, col):
    return [(r, c) for r, c in [(row,col-1),(row+1,col),(row,col+1),(row-1,col)] if 0 <= r < len(grid) and 0 <= c < len(grid[row])]

def get_basin(row, col):
    cells = [(row, col)]
    used.append((row, col))
    size = 0
    while len(cells) > 0:
        r, c = cells.pop()
        size += 1
        for ra, ca in get_adjacents(r, c):
            if grid[ra][ca] != 9 and (ra, ca) not in used:
                used.append((ra, ca))
                cells.append((ra, ca))
    return size

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

    grid = [[int(v) for v in list(l)] for l in lines]

##########
# part 1 #
##########
    lowest_points = [grid[r][c] for r in range(len(grid)) for c in range(len(grid[r])) if all([grid[r][c] < grid[ra][ca] for ra, ca in get_adjacents(r, c)])]
    print(sum([l+1 for l in lowest_points]))

##########
# part 2 #
##########
    used = []
    basin_sizes = [get_basin(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] != 9 and (r, c) not in used]
    basin_sizes.sort(reverse=True)
    print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])
