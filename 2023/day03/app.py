import os
import re
import math


def get_surround(grid, r, a, b):
    y_s = r - 1
    y_e = r + 1
    x_s = a - 1
    x_e = b + 1
    number_pos = [(r, n) for n in range(a, b + 1)]
    return [
        grid[y][x]
        for y in range(y_s, y_e + 1)
        for x in range(x_s, x_e + 1)
        if y >= 0
        and x >= 0
        and y < len(grid)
        and x < len(grid[0])
        and (y, x) not in number_pos
        and grid[y][x] != "."
    ]


def get_adjacent(y, x):
    return set(
        [
            (b, a)
            for b in range(y - 1, y + 2)
            for a in range(x - 1, x + 2)
            if b != y or a != x
        ]
    )


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = [line.strip() for line in file.readlines()]
    grid = [[*line] for line in lines]

    ##########
    # part 1 #
    ##########
    part_1 = 0
    for i, line in enumerate(lines):
        for match in re.finditer(r"\d+", line):
            if (
                len(
                    get_surround(
                        grid, i, match.start(), match.start() + len(match.group()) - 1
                    )
                )
                > 0
            ):
                part_1 += int(match.group())
    print(part_1)

    ##########
    # part 2 #
    ##########
    numbers = [
        (
            int(match.group()),
            set(
                [
                    (i, n)
                    for n in range(match.start(), match.start() + len(match.group()))
                ]
            ),
        )
        for i, line in enumerate(lines)
        for match in re.finditer(r"\d+", line)
    ]
    gears = [
        get_adjacent(y, x)
        for y, line in enumerate(grid)
        for x, c in enumerate(line)
        if c == "*"
    ]
    part_2 = 0
    for gear in gears:
        adj_parts = [n for n, pos in numbers if len(gear.intersection(pos)) > 0]
        if len(adj_parts) == 2:
            part_2 += math.prod(adj_parts)
    print(part_2)


if __name__ == "__main__":
    main()
