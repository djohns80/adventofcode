def calculate_costs():
    points = [(0, 0, 0)]
    risks = {}
    while points:
        risk, x, y = points.pop(0)
        for xx,yy in [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]:
            if 0 <= yy < len(grid) and 0 <= xx < len(grid[0]):
                new_cost = risk + grid[xx][yy]
                if (xx,yy) not in risks or risks[(xx,yy)] > new_cost:
                    risks[(xx,yy)] = new_cost
                    points.append((new_cost,xx,yy))
        points = sorted(points)
    return risks[(len(grid[0])-1,len(grid)-1)]

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]
    grid = [[int(v) for v in r] for r in lines]

##########
# part 1 #
##########
    print(calculate_costs())

##########
# part 2 #
##########
    grid = [[(v+i+j if v+i+j <=9 else v+i+j-9) for i in range(5) for v in r] for j in range(5) for r in grid]

    print(calculate_costs())