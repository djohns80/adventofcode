import math

def gcdExtended(a, b):
    if a == 0 :
        return b,0,1
    gcd, x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

    depart = int(lines[0])
    buses = [l for l in lines[1].split(',')]

############
### part 1 #
############
    next_departs = [(int(b), (int(depart/int(b))+1)*int(b) - depart) for b in buses if b != 'x']
    next_departs.sort(key=lambda tup: tup[1])
    print(next_departs[0][0] * next_departs[0][1])

###########
## part 2 #
###########
    buses = [t for t in [(int(b), n) if b != 'x' else None for n, b in enumerate(buses)] if t is not None]
    prod = math.prod([b[0] for b in buses])
    result = sum([r * (gcdExtended(int(prod/n), n)[1] % n) * int(prod/n) for n, r in buses])
    print(-result % prod)
