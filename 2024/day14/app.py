import os
import re
import math


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = content.splitlines()
    robots = {}
    for n, line in enumerate(lines):
        values = list(map(int, re.findall(r"-?\d+", line)))
        robots[n] = {
            "pos": (values[0] + values[1] * 1j),
            "vel": (values[2] + values[3] * 1j),
        }
    dim = 101 + 103j

    ##########
    # part 1 #
    ##########
    seconds = 100
    for robot in robots.values():
        robot["pos"] = robot["pos"] + (robot["vel"] * seconds)
        robot["pos"] = (robot["pos"].real % dim.real) + (
            robot["pos"].imag % dim.imag
        ) * 1j
    quadrants = [[0] * 2 for _ in range(2)]
    for robot in robots.values():
        if (robot["pos"].real / (dim.real // 2) != 1.0) and (
            robot["pos"].imag / (dim.imag // 2) != 1.0
        ):
            quadrants[0 if int(robot["pos"].imag / (dim.imag // 2)) < 1 else 1][
                0 if int(robot["pos"].real / (dim.real // 2)) < 1 else 1
            ] += 1
    print(math.prod(c for r in quadrants for c in r))

    ##########
    # part 2 #
    ##########
    n = 100
    stop_searching = False
    while not stop_searching:
        n += 1
        dim = 101 + 103j
        for robot in robots.values():
            robot["pos"] += robot["vel"]
            robot["pos"] = (robot["pos"].real % dim.real) + (
                robot["pos"].imag % dim.imag
            ) * 1j

        grid = [[0] * int(dim.real) for _ in range(int(dim.imag))]
        for robot in robots.values():
            grid[int(robot["pos"].imag)][int(robot["pos"].real)] += 1
        stop_searching = any(
            [
                True
                for line in grid
                if "##########" in "".join(["#" if c > 0 else " " for c in line])
            ]
        )
        if stop_searching:
            print(n)
            for line in grid:
                print("".join(["#" if c > 0 else " " for c in line]))


if __name__ == "__main__":
    main()
