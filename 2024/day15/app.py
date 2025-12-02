import os
from collections import deque

directions = {
    "<": -1,
    ">": 1,
    "^": -1j,
    "v": 1j,
}


def print_warehouse(warehouse, rows, cols):
    for y in range(rows):
        print("".join(warehouse[x + (y * 1j)] for x in range(cols)))


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = content.split("\n\n")

    ##########
    # part 1 #
    ##########
    warehouse = {
        (x + (y * 1j)): c
        for y, line in enumerate(lines[0].splitlines())
        for x, c in enumerate(line)
    }
    robot = [p for p, v in warehouse.items() if v == "@"][0]
    moves = deque([directions[c] for c in "".join(lines[1].splitlines())])
    while moves:
        move = moves.popleft()
        if warehouse[robot + move] == ".":
            warehouse[robot] = "."
            robot += move
            warehouse[robot] = "@"
        elif warehouse[robot + move] == "#":
            continue
        elif warehouse[robot + move] == "O":
            n = 2
            while warehouse[robot + (move * n)] not in ["#", "."]:
                n += 1
            if warehouse[robot + (move * n)] == "#":
                continue
            else:
                warehouse[robot + (move * n)] = "O"
                warehouse[robot + move] = "."
                warehouse[robot] = "."
                robot += move
                warehouse[robot] = "@"
    print(sum(int(p.real + (p.imag * 100)) for p, v in warehouse.items() if v == "O"))

    ##########
    # part 2 #
    ##########


if __name__ == "__main__":
    main()
