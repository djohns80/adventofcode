import numpy as np

def parse_lines(data):
    dicts = []
    for line in data:
        split_line = line.split('->')
        x1, y1 = split_line[0].strip().split(',')
        x2, y2 = split_line[1].strip().split(',')
        dicts.append({'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2),})
    return dicts

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

    lines = parse_lines(lines)

    max_x = max([x for a in [[l['x1'], l['x2']] for l in lines] for x in a])
    max_y = max([y for a in [[l['y1'], l['y2']] for l in lines] for y in a])
    coords = np.zeros([max_y + 1, max_x + 1])

    for s in lines:
        if s['x1'] == s['x2']:
            step = 1 if s['y2'] > s['y1'] else -1
            for y in range(s['y1'], s['y2']+step, step):
                coords[y][s['x1']] += 1
        elif s['y1'] == s['y2']:
            step = 1 if s['x2'] > s['x1'] else -1
            for x in range(s['x1'], s['x2']+step, step):
                coords[s['y1']][x] += 1

#    for y in coords:
#        print(' '.join([str(int(v)) if v != 0 else '.' for v in y]))

    more_than_two_count = len([int(x) for y in coords for x in y if x >= 2])
    print(more_than_two_count)
