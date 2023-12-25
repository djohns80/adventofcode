import os
import copy


file = open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
    "r",
    encoding="utf-8",
)
data = list(map(str.strip, file.readlines()))
for i in range(len(data)):
    data[i] = data[i].split("~")
    data[i] = [x.split(",") for x in data[i]]
for j in range(len(data)):
    for k in range(len(data[j])):
        for l in range(len(data[j][k])):
            data[j][k][l] = int(data[j][k][l])

cubes = dict()
bricks = dict()

for m in range(len(data)):
    brick = []
    if data[m][0][0] != data[m][1][0]:
        for c in range(
            min(data[m][0][0], data[m][1][0]), max(data[m][0][0], data[m][1][0]) + 1
        ):
            cubes[(c, data[m][0][1], data[m][0][2])] = m
            brick.append([c, data[m][0][1], data[m][0][2]])
        bricks[m] = brick
    elif data[m][0][1] != data[m][1][1]:
        for d in range(
            min(data[m][0][1], data[m][1][1]), max(data[m][0][1], data[m][1][1]) + 1
        ):
            cubes[(data[m][0][0], d, data[m][0][2])] = m
            brick.append([data[m][0][0], d, data[m][0][2]])
        bricks[m] = brick
    elif data[m][0][2] != data[m][1][2]:
        for e in range(
            min(data[m][0][2], data[m][1][2]), max(data[m][0][2], data[m][1][2]) + 1
        ):
            cubes[(data[m][0][0], data[m][0][1], e)] = m
            brick.append([data[m][0][0], data[m][0][1], e])
        bricks[m] = brick
    else:
        cubes[(data[m][0][0], data[m][0][1], data[m][0][2])] = m
        bricks[m] = [[data[m][0][0], data[m][0][1], data[m][0][2]]]

changed = True
while changed:
    changed = False
    sortedBricks = sorted(bricks.items(), key=lambda f: f[1][0][2])
    for key, val in sortedBricks:
        if val[0][2] == 1:
            continue
        else:
            for sq in val:
                nsq = tuple([sq[0], sq[1], sq[2] - 1])
                if nsq in cubes.keys():
                    if cubes.get(nsq) == key:
                        pass
                    else:
                        break
                else:
                    pass
            else:
                nbrick = []
                for vsq in val:
                    nvsq = tuple([vsq[0], vsq[1], vsq[2] - 1])
                    cubes.pop(tuple(vsq))
                    cubes[nvsq] = key
                    nbrick.append(list(nvsq))
                bricks[key] = nbrick
                changed = True

sortedBricks = sorted(bricks.items(), key=lambda f: f[1][0][2])
breakable = dict()
loadbearing = dict()
for fkey, fval in sortedBricks:
    supports = set()
    if fval[0][2] == 1:
        continue
    else:
        for sqr in fval:
            fsq = tuple([sqr[0], sqr[1], sqr[2] - 1])
            if fsq in cubes.keys():
                if cubes.get(fsq) == fkey:
                    pass
                else:
                    supports.add(cubes.get(fsq))
            else:
                pass
    if len(supports) == 0 and fval[0][2] != 1:
        raise RuntimeError
    elif len(supports) == 1:
        for ssup in supports:
            if ssup in breakable.keys():
                breakable.pop(ssup)
            loadbearing[ssup] = fkey
    else:
        for sup in supports:
            if sup not in loadbearing.keys():
                breakable[sup] = fkey

for ffkey, ffval in sortedBricks:  # add bricks that don't support any other brick
    if ffkey not in loadbearing.keys() and ffkey not in breakable.keys():
        breakable[ffkey] = -1

print("part1: ", len(breakable))


def waterfall(
    wbricks, wcubes
):  # copypasted from p1, just changed variable names for easier debugging
    falling = set()
    wchanged = True
    while wchanged:
        wchanged = False
        wsortedBricks = sorted(wbricks.items(), key=lambda f: f[1][0][2])
        for wkey, wval in wsortedBricks:
            if wval[0][2] == 1:
                continue
            else:
                for wsq in wval:
                    wnsq = tuple([wsq[0], wsq[1], wsq[2] - 1])
                    if wnsq in wcubes.keys():
                        if wcubes.get(wnsq) == wkey:
                            pass
                        else:
                            break
                    else:
                        pass
                else:
                    wnbrick = []
                    for wvsq in wval:
                        wnvsq = tuple([wvsq[0], wvsq[1], wvsq[2] - 1])
                        wcubes.pop(tuple(wvsq))
                        wcubes[wnvsq] = wkey
                        wnbrick.append(list(wnvsq))
                    wbricks[wkey] = wnbrick
                    falling.add(wkey)
                    wchanged = True
    return len(falling)


result = 0
for load in loadbearing.keys():
    newbricks = copy.deepcopy(bricks)
    newcubes = copy.deepcopy(cubes)
    toRem = newbricks.get(load)
    for rem in toRem:
        newcubes.pop(tuple(rem))
    newbricks.pop(load)
    result += waterfall(newbricks, newcubes)

print("part2: ", result)
