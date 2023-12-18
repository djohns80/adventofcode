import os
import re

directions = {
    "L": (0, -1),
    "R": (0, 1),
    "U": (-1, 0),
    "D": (1, 0),
}


def get_direction(num):
    match num:
        case 0:
            return "R"
        case 1:
            return "D"
        case 2:
            return "L"
        case 3:
            return "U"


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = map(str.strip, file.readlines())

    ##########
    # part 1 #
    ##########
    data = []
    for line in lines:
        match = re.match(
            r"(?P<dir>[U|D|L|R])\s(?P<num>\d+)\s\((?P<col>#[0-9a-f]+)\)", line
        )
        if match:
            data.append(match.groupdict())
    pos = (0, 0)
    vertices = [pos]
    for m in data:
        for _ in range(int(m["num"])):
            d = directions[m["dir"]]
            pos = (pos[0] + d[0], pos[1] + d[1])
        vertices.append(pos)
    A = (
        abs(
            sum(
                pair[0][1] * pair[1][0] - pair[0][0] * pair[1][1]
                for pair in zip(vertices[1:], vertices)
            )
        )
        / 2
    )
    b = sum(int(d["num"]) for d in data)
    i = A - (b / 2) + 1
    print(int(i + b))

    ##########
    # part 2 #
    ##########
    new_data = [
        {"dir": get_direction(int(d["col"][-1])), "num": int(d["col"][1:6], 16)}
        for d in data
    ]
    pos = (0, 0)
    vertices_2 = [pos]
    for m in new_data:
        for _ in range(int(m["num"])):
            d = directions[m["dir"]]
            pos = (pos[0] + d[0], pos[1] + d[1])
        vertices_2.append(pos)
    A_2 = (
        abs(
            sum(
                pair[0][1] * pair[1][0] - pair[0][0] * pair[1][1]
                for pair in zip(vertices_2[1:], vertices_2)
            )
        )
        / 2
    )
    b_2 = sum(int(d["num"]) for d in new_data)
    i_2 = A_2 - (b_2 / 2) + 1
    print(int(i_2 + b_2))


if __name__ == "__main__":
    main()
