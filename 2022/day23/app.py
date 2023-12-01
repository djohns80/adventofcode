import os
from collections import Counter
from collections import deque
from itertools import count

vectors = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1),
    'NE': (-1, 1),
    'NW': (-1, -1),
    'SE': (1, 1),
    'SW': (1, -1),
}

def parse_field(s):
    field = set()
    for r, line in enumerate(s.splitlines()):
        for c, tile in enumerate(line):
            if tile == '#':
                field.add((r, c))
    return field

def all_empty(field, pos):
    r, c = pos
    for dr, dc in vectors.values():
        if (r + dr, c + dc) in field:
            return False
    return True

def move_allowed(field, pos, directions):
    r, c = pos
    for dr, dc in (vectors[d] for d in directions):
        nr, nc = r + dr, c + dc
        if (nr, nc) in field:
            return False
    return nr, nc

def move_n(field, pos):
    if new := move_allowed(field, pos, ('NE', 'NW', 'N')):
        return new

def move_s(field, pos):
    if new := move_allowed(field, pos, ('SE', 'SW', 'S')):
        return new

def move_w(field, pos):
    if new := move_allowed(field, pos, ('NW', 'SW', 'W')):
        return new

def move_e(field, pos):
    if new := move_allowed(field, pos, ('NE', 'SE', 'E')):
        return new

def solve(s: str, rounds):
    field = parse_field(s)
    moves = deque((move_n, move_s, move_w, move_e))
    for rnd in rounds:
        proposals = []
        for pos in field:
            if not all_empty(field, pos):
                for func in moves:
                    if new_pos := func(field, pos):
                        break
                else:
                    new_pos = pos
            else:
                new_pos = pos
            proposals.append(new_pos)
        c = Counter(proposals)
        new_field = set(new_e if c[new_e] == 1 else e for e, new_e in zip(field, proposals))
        if field == new_field:
            return rnd
        field = new_field
        moves.rotate(-1)
    rmin = min(r for r, c in field)
    cmin = min(c for r, c in field)
    rmax = max(r for r, c in field)
    cmax = max(c for r, c in field)
    area = (rmax - rmin + 1) * (cmax - cmin + 1)
    return area - len(field)

if __name__ == '__main__':
    DATA = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input'), 'r', encoding='utf-8').read()

    print(solve(DATA, rounds=range(10)))
    print(solve(DATA, rounds=count(1)))



# import argparse
# import os
# from collections import deque
# from collections import Counter

# MOVES = {
#     'NW': (-1, -1),
#     'N': (0, -1),
#     'NE': (1, -1),
#     'W': (-1, 0),
#     'E': (1, 0),
#     'SW': (-1, 1),
#     'S': (0, 1),
#     'SE': (1, 1)
# }

# def surround_empty(g, e):
#     return not any((e[0] + dx, e[1] + dy) in g for dx, dy in MOVES.values())

# def move_allowed(g, e, m):
#     for dx, dy in (MOVES[d] for d in m):
#         new_e = (e[0] + dx, e[1] + dy)
#         if new_e in g:
#             return False
#     return new_e

# def move_n(g, e):
#     if new_e := move_allowed(g, e, ['NW', 'N', 'NE']):
#         return new_e

# def move_s(g, e):
#     if new_e := move_allowed(g, e, ['SW', 'S', 'SE']):
#         return new_e

# def move_w(g, e):
#     if new_e := move_allowed(g, e, ['NW', 'W', 'SW']):
#         return new_e

# def move_e(g, e):
#     if new_e := move_allowed(g, e, ['NE', 'E', 'SE']):
#         return new_e

# def main(input_file):
#     file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
#     elves = set((x,y) for y, l in enumerate(file.read().splitlines()) for x, c in enumerate(l) if c == '#')
#     moves = deque((move_n, move_s, move_w, move_e))

# ##########
# # part 1 #
# ##########
#     for n in range(10):
#         proposals = []
#         for e in elves:
#             if not surround_empty(elves, e):
#                 for func in moves:
#                     if new_e := func(elves, e):
#                         break
#                 else:
#                     new_e = e
#             else:
#                 new_e = e
#             proposals.append(new_e)
#         c = Counter(proposals)
#         new_elves = set(new_e if c[new_e] == 1 else e for e, new_e in zip(elves, proposals))
#         if elves == new_elves:
#             print(n)
#         elves = new_elves
#         moves.rotate(-1)
#     min_x = min(x for x, _ in elves)
#     min_y = min(y for _, y in elves)
#     max_x = max(x for x, _ in elves)
#     max_y = max(y for _, y in elves)
#     area = (max_x - min_x + 1) * (max_y - min_y + 1)
#     print(area - len(elves))

# ##########
# # part 2 #
# ##########


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     group = parser.add_mutually_exclusive_group()
#     group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
#     group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
#     parser.set_defaults(input='input')
#     args = parser.parse_args()
#     main(args.input)
