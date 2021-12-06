import re

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = [m.groupdict() for m in re.finditer(r'(?P<x1>\d+),(?P<y1>\d+)\s->\s(?P<x2>\d+),(?P<y2>\d+)', file.read())]
    lines = [{'x1': int(l['x1']), 'y1': int(l['y1']), 'x2': int(l['x2']), 'y2': int(l['y2'])} for l in lines]

    max_x = max([x for a in [[l['x1'], l['x2']] for l in lines] for x in a])
    max_y = max([y for a in [[l['y1'], l['y2']] for l in lines] for y in a])
    coords = [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]

    for s in lines:
        if s['x1'] == s['x2']:
            step = 1 if s['y2'] > s['y1'] else -1
            for y in range(s['y1'], s['y2']+step, step):
                coords[y][s['x1']] += 1
        elif s['y1'] == s['y2']:
            step = 1 if s['x2'] > s['x1'] else -1
            for x in range(s['x1'], s['x2']+step, step):
                coords[s['y1']][x] += 1
###########
## part 2 #
###########
        else:
            step_y = 1 if s['y2'] > s['y1'] else -1
            step_x = 1 if s['x2'] > s['x1'] else -1
            x = s['x1']
            y = s['y1']
            while x != s['x2'] and y != s['y2']:
                coords[y][x] += 1
                x += step_x
                y += step_y
            coords[y][x] += 1

#    for y in coords:
#        print(' '.join([str(int(v)) if v != 0 else '.' for v in y]))

    more_than_two_count = len([int(x) for y in coords for x in y if x >= 2])
    print(more_than_two_count)
