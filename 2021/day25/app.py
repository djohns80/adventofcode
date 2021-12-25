if __name__ == '__main__':
#    file = open('sample', 'r', encoding='utf-8')
    file = open('input', 'r', encoding='utf-8')
    lines = file.readlines()
    grid = [list(l.strip()) for l in lines]

##########
# part 1 #
##########
    steps = 1
    while True:
        new_grid = []
        for y,r in enumerate(grid):
            for x,c in enumerate(r):
                next_x = (x+1) % len(r)
                if c == '>' and r[next_x] == '.':
                    new_grid.append((y, x, next_x))
        for y,x,next_x in new_grid:
            grid[y][x] = '.'
            grid[y][next_x] = '>'
        east_still = not new_grid
        new_grid = []
        for y,r in enumerate(grid):
            for x,c in enumerate(r):
                next_y = (y+1) % len(grid)
                if c == 'v' and grid[next_y][x] == '.':
                    new_grid.append((y, x, next_y))
        if east_still and not new_grid:
            break
        for y, x, next_y in new_grid:
            grid[y][x]    = '.'
            grid[next_y][x] = 'v'
        steps += 1
    print(steps)
