import re
import itertools
from collections import defaultdict

def rotate_point(v):
    r = lambda a, b, c: (a, c, -b)
    t = lambda a, b, c: (-b, a, c)
    a = []
    for _ in range(2):
        for _ in range(3):
            v = r(*v)
            a.append(v)
            for _ in range(3):
                v = t(*v)
                a.append(v)
        v = r(*t(*r(*v)))
    return a

def oo(aa, bb):
    print(aa,bb)
    ptsa = set(aa)
    for (a, b, c), (d, e, f) in itertools.product(aa, bb):
        if len(ptsa.intersection((x - d + a, y - e + b, z - f + c) for x, y, z in bb)) == 12:
            return d - a, e - b, f - c

def process_data(data):
    fr = {0: 0}
    scanners = {0: (0, 0, 0)}
    nt = defaultdict(set)
    beacons = set(data[0][0])
    while len(fr) < len(data):
        for i, sci in data.items():
            if i in fr:
                continue
            for j, jrotidx in [*fr.items()]:
                if j in nt[i]:
                    continue
                scj = data[j][jrotidx]
                axx, ayy, azz = scanners[j]
                for rot_idx in range(24):
                    res = oo(scj, sci[rot_idx])
                    if res is None:
                        continue
                    ox, oy, oz = res
                    beacons |= {(x - ox - axx, y - oy - ayy, z - oz - azz) for x, y, z in sci[rot_idx]}
                    fr[i] = rot_idx
                    scanners[i] = ox + axx, oy + ayy, oz + azz
                    break
                else:
                    continue
                break
            else:
                nt[i].add(j)
                continue
            break
    return scanners, beacons

if __name__ == '__main__':
    file = open('sample', 'r')
#    file = open('input', 'r')
    lines = file.read()

    scanner_data = {int(re.search(r'\d+', l.splitlines()[0]).group()): [tuple(int(v) for v in c.split(','))for c in l.splitlines()[1:]] for l in lines.split('\n\n')}
    scanner_data = {k: [*zip(*[rotate_point(p) for p in v])] for k,v in scanner_data.items()}

##########
# part 1 #
##########
    results = process_data(scanner_data)
    print(len(results[1]))

##########
# part 1 #
##########
    print(max([sum([abs(i - j) for i,j in zip(*[av, bv])]) for ai,av in enumerate(results[0].values()) for bv in list(results[0].values())[ai:] if av != bv]))
