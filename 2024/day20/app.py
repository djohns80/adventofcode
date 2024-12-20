import os


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = content.splitlines()
    start, end = None, None
    track_nodes = set()
    walls = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            match c:
                case "S":
                    start = complex(x, y)
                case "E":
                    end = complex(x, y)
                case ".":
                    track_nodes.add(complex(x, y))
                case "#":
                    walls.add(complex(x, y))
    path = [start]
    while track_nodes:
        next_node = [n for n in track_nodes if abs(n - path[-1]) == 1][0]
        path.append(next_node)
        track_nodes.remove(next_node)
    if abs(end - path[-1]) == 1:
        path.append(end)
    else:
        raise ValueError("Invalid path found")

    ##########
    # part 1 #
    ##########
    min_saving = 100
    cheats = set(
        ((a, b), m + min_saving)
        for n, a in enumerate(path)
        for m, b in enumerate(path[n + min_saving + 2 :])
        if (m + min_saving) > 0 and abs(a - b) == 2
    )
    print(len(cheats))

    # ##########
    # # part 2 #
    # ##########
    min_saving = 100
    cheat_duration = 20
    cheats = set(
        ((a, b), m + min_saving + 2 - int(abs(a.real - b.real) + abs(a.imag - b.imag)))
        for n, a in enumerate(path)
        for m, b in enumerate(path[n + min_saving + 2 :])
        if (m + min_saving + 2 - int(abs(a.real - b.real) + abs(a.imag - b.imag)))
        >= min_saving
        and abs(a.real - b.real) + abs(a.imag - b.imag) <= cheat_duration
    )
    print(len(cheats))


if __name__ == "__main__":
    main()
