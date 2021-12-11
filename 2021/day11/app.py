def get_adjacents(row, col):
    return [(r, c) for r, c in [(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1,col),(row+1,col+1)] if 0 <= r < len(grid) and 0 <= c < len(grid[row])]

def perform_step():
    for y, r in enumerate(grid):
        for x in range(len(r)):
            grid[y][x] += 1
    flashed = set()
    while True:
        changes = 0
        for y, r in enumerate(grid):
            for x, v in enumerate(r):
                if v > 9:
                    flashed.add((y,x))
                    grid[y][x] = 0
                    for p in get_adjacents(y, x):
                        changes += 1
                        grid[p[0]][p[1]] += 1
        if changes == 0:
            break
    for p in flashed:
        grid[p[0]][p[1]] = 0
    return len(flashed)

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

##########
# part 1 #
##########
    grid = [[int(v) for v in list(l)] for l in lines]
    flash_count = 0
    for s in range(100):
        flashes = perform_step()
        flash_count += flashes
    print(flash_count)

##########
# part 2 #
##########
    grid = [[int(v) for v in list(l)] for l in lines]
    s = 0
    while True:
        flashes = perform_step()
        if flashes == 100:
            break
        s += 1
    print(s+1)
