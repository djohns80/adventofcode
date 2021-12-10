import copy

def seating_round(part=1):
    grid_temp = copy.deepcopy(grid)
    for r, row in enumerate(grid):
        for c, space in enumerate(row):
            occupied_adjacents = get_adjacents(r,c) if part == 1 else get_visible(r,c)
            if space == 'L' and len(occupied_adjacents) == 0:
                grid_temp[r][c] = '#'
            elif space == '#' and len(occupied_adjacents) >= (4 if part == 1 else 5):
                grid_temp[r][c] = 'L'
    return grid_temp

def get_adjacents(row, col):
    return [grid[r][c] for r, c in [(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1,col),(row+1,col+1)] if 0 <= r < len(grid) and 0 <= c < len(grid[row]) and grid[r][c] == '#']

def get_visible(row, col):
    results = []
    for ir, ic in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        n = 1
        while True:
            r = row + (ir*n)
            c = col + (ic*n)
            if 0 <= r < len(grid) and 0 <= c < len(grid[row]):
                if grid[r][c] != '.':
                    if grid[r][c] == '#':
                        results.append(grid[r][c])
                    break
                n += 1
            else:
                break
    return results

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

##########
# part 1 #
##########
    grid = [list(line) for line in lines]
    old_grid = None
    while grid != old_grid:
        old_grid = copy.deepcopy(grid)
        grid = seating_round()
    occupied_seat_counts = [len(r) - len(''.join(r).replace('#','')) for r in grid]
    print(sum(occupied_seat_counts))

##########
# part 2 #
##########
    grid = [list(line) for line in lines]
    old_grid = None
    while grid != old_grid:
        old_grid = copy.deepcopy(grid)
        grid = seating_round(2)
    occupied_seat_counts = [len(r) - len(''.join(r).replace('#','')) for r in grid]
    print(sum(occupied_seat_counts))
