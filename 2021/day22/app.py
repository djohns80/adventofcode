import re
from collections import defaultdict

if __name__ == '__main__':
    file = open('sample', 'r')
#    file = open('input', 'r')
    data = file.read()
    lines = [m.groupdict() for m in re.finditer(r'(?P<action>on|off)\sx=(?P<x_min>-?\d+)\.\.(?P<x_max>-?\d+),y=(?P<y_min>-?\d+)\.\.(?P<y_max>-?\d+),z=(?P<z_min>-?\d+)\.\.(?P<z_max>-?\d+)', data)]
    lines = [{'action': l['action'], 'x_min': int(l['x_min']), 'x_max': int(l['x_max']), 'y_min': int(l['y_min']), 'y_max': int(l['y_max']), 'z_min': int(l['z_min']), 'z_max': int(l['z_max'])} for l in lines]

##########
# part 1 #
##########
    on_cubes = set()
    for l in lines:
        if all([-50 <= r <= 50 for r in [l['x_min'], l['x_max'], l['y_min'], l['y_max'], l['z_min'], l['z_max']]]):
            cubes = set([(x, y, z) for x in range(l['x_min'], l['x_max']+1) for y in range(l['y_min'], l['y_max']+1) for z in range(l['z_min'], l['z_max']+1) if -50 <= x <= 50 and -50 <= y <= 50 and -50 <= z <= 50])
            if l['action'] == 'on':
                on_cubes.update(cubes)
            elif l['action'] == 'off':
                on_cubes.difference_update(cubes)
    print(len(on_cubes))

##########
# part 2 #
##########
    cubes = defaultdict(int)
    for l in lines:
        nsgn = 1 if l['action'] == 'on' else -1
        update = defaultdict(int)
        for (ex0, ex1, ey0, ey1, ez0, ez1), esgn in cubes.items():
            ix0 = max(l['x_min'], ex0)
            ix1 = min(l['x_max'], ex1)
            iy0 = max(l['y_min'], ey0)
            iy1 = min(l['y_max'], ey1)
            iz0 = max(l['z_min'], ez0)
            iz1 = min(l['z_max'], ez1)
            if ix0 <= ix1 and iy0 <= iy1 and iz0 <= iz1:
                update[(ix0, ix1, iy0, iy1, iz0, iz1)] -= esgn
        if nsgn > 0:
            update[(l['x_min'], l['x_max'], l['y_min'], l['y_max'], l['z_min'], l['z_max'])] += nsgn
        cubes.update(update)

    print(sum((x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1) * sgn for (x0, x1, y0, y1, z0, z1), sgn in cubes.items()))
