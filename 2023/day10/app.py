import os


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))
    grid = {
        (y, x): c
        for y, line in enumerate(lines)
        for x, c in enumerate(list(line.strip()))
    }
    start = [k for k, v in grid.items() if v == "S"][0]

    def connections(y, x):
        match grid[(y, x)]:
            case "|":
                options = [(y - 1, x), (y + 1, x)]  # N-S
            case "-":
                options = [(y, x + 1), (y, x - 1)]  # E-W
            case "L":
                options = [(y - 1, x), (y, x + 1)]  # N-E
            case "J":
                options = [(y - 1, x), (y, x - 1)]  # N-W
            case "7":
                options = [(y + 1, x), (y, x - 1)]  # S-W
            case "F":
                options = [(y + 1, x), (y, x + 1)]  # S-E
            case _:
                options = []
        return [o for o in options if o in grid]

    def get_start_options(y, x):
        options = [
            (y + dy, x + dx)
            for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if (y + dy, x + dx) in grid
        ]
        return [o for o in options if (y, x) in connections(*o)]

    ##########
    # part 1 #
    ##########
    path = [start]
    pos = get_start_options(*start)[0]
    while grid[pos] != "S":
        path.append(pos)
        pos = [p for p in connections(*pos) if p != path[-2]][0]
    print(int(len(path) / 2))

    ##########
    # part 2 #
    ##########
    part_2 = 0
    for y in range(len(lines)):
        inside = False
        for x in range(len(lines[0])):
            if (y, x) in path:
                if grid[(y, x)] in "|JL":
                    inside = not inside
            else:
                part_2 += inside
    print(part_2)


if __name__ == "__main__":
    main()
