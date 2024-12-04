import os
from collections import defaultdict
import re


def count_xmas(grid, x, y):
    vectors = [
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ]
    words = [
        "".join([grid[(x + (i * v[0]), y + (i * v[1]))] for i in range(4)])
        for v in vectors
    ]
    return len([w for w in words if w == "XMAS"])


def check_mas(grid, x, y):
    vectors = [
        (1, 1),
        (1, -1),
        (-1, -1),
        (-1, 1),
    ]
    count_mas = sum(
        1
        for v in vectors
        if grid[(x + (-1 * v[0]), y + (-1 * v[1]))] == "M"
        and grid[(x + (1 * v[0]), y + (1 * v[1]))] == "S"
    )
    return count_mas == 2


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    grid = defaultdict(lambda: "")
    for y, line in enumerate(content.splitlines()):
        for x, char in enumerate(line.strip()):
            grid[(x, y)] = char
    row_count = len(content.splitlines())
    col_count = len(content.splitlines()[0])

    ##########
    # part 1 #
    ##########
    print(sum(count_xmas(grid, x, y) for x in range(row_count) for y in range(col_count) if grid[(x, y)] == "X"))

    ##########
    # part 2 #
    ##########
    print(sum(check_mas(grid, x, y) for x in range(row_count) for y in range(col_count) if grid[(x, y)] == "A"))


if __name__ == "__main__":
    main()
