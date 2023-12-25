import os


def shadow(d):
    return ((d[0][0], d[0][1], d[0][2] - 1), (d[1][0], d[1][1], d[1][2] - 1))

def brick(a, b):
    xa, ya, za = a
    xb, yb, zb = b
    return [(x, y, z) for z in range(za, zb + 1) for y in range(ya, yb + 1) for x in range(xa, xb + 1)]

def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))
    blocks = [
        (
            tuple(map(int, line.split("~")[0].split(","))),
            tuple(map(int, line.split("~")[1].split(","))),
        )
        for line in lines
    ]
    blocks.sort(key=lambda b: b[0][2]) # sort blocks
    # min_x = min(min([b[0][0], b[1][0]]) for b in blocks)
    # max_x = max(max([b[0][0], b[1][0]]) for b in blocks)
    # min_y = min(min([b[0][1], b[1][1]]) for b in blocks)
    # max_y = max(max([b[0][1], b[1][1]]) for b in blocks)
    min_z = min(min([b[0][2], b[1][2]]) for b in blocks)
    max_z = max(max([b[0][2], b[1][2]]) for b in blocks)

    ##########
    # part 1 #
    ##########
    for b in blocks:
        if b[0][2] != 1 and b[1][2] != 1:
            print(b, shadow(b))

    ##########
    # part 2 #
    ##########


if __name__ == "__main__":
    main()
