import os
import re


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str((self.x, self.y, self.z))


class Hailstone:
    def __init__(self, px, py, pz, vx, vy, vz):
        self.p = Point(px, py, pz)
        self.v = Point(vx, vy, vz)

    def __str__(self):
        return (
            f"{self.p.x}, {self.p.y}, {self.p.z} @  {self.v.x}, {self.v.y}, {self.v.z}"
        )


def intersection(a, b, z=False):
    if (a.v.x * b.v.y) != (b.v.x * a.v.y):
        t_b = (
            (b.p.x * a.v.y) - (a.p.x * a.v.y) - (a.v.x * b.p.y) + (a.v.x * a.p.y)
        ) / ((a.v.x * b.v.y) - (b.v.x * a.v.y))
        t_a = (b.p.x + (b.v.x * t_b) - a.p.x) / a.v.x
    elif z and (a.v.x * b.v.z) != (b.v.x * a.v.z):
        t_b = (
            (b.p.x * a.v.z) - (a.p.x * a.v.z) - (a.v.x * b.p.z) + (a.v.x * a.p.z)
        ) / ((a.v.x * b.v.z) - (b.v.x * a.v.z))
        t_a = (b.p.x + (b.v.x * t_b) - a.p.x) / a.v.x
    elif z and (a.v.y * b.v.z) != (b.v.y * a.v.z):
        t_b = (
            (b.p.y * a.v.z) - (a.p.y * a.v.z) - (a.v.y * b.p.z) + (a.v.y * a.p.z)
        ) / ((a.v.y * b.v.y) - (b.v.y * a.v.y))
        t_a = (b.p.y + (b.v.y * t_b) - a.p.y) / a.v.y
    else:
        print(a, b)
        return None
    return (
        Point(a.p.x + (a.v.x * t_a), a.p.y + (a.v.y * t_a), a.p.z + (a.v.z * t_a)),
        t_a,
        t_b,
    )


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    hailstones = [
        Hailstone(*map(int, m.groupdict().values()))
        for m in re.finditer(
            r"(?P<px>-?\d+),\s+(?P<py>-?\d+),\s+(?P<pz>-?\d+)\s+@\s+(?P<vx>-?\d+),\s+(?P<vy>-?\d+),\s+(?P<vz>-?\d+)",
            file.read(),
        )
    ]

    ##########
    # part 1 #
    ##########
    part_1 = 0
    # rng = (7, 27)
    rng = (200000000000000, 400000000000000)
    for n, h in enumerate(hailstones):
        for i in range(n + 1, len(hailstones)):
            cross = intersection(hailstones[n], hailstones[i])
            if cross:
                if rng[0] <= cross[0].x <= rng[-1] and rng[0] <= cross[0].y <= rng[-1]:
                    if cross[1] > 0 and cross[2] > 0:
                        part_1 += 1
    print(part_1)

    ##########
    # part 2 #
    ##########


if __name__ == "__main__":
    main()
