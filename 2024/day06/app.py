import os
from collections import defaultdict


def in_front(pos, fac, grid):
    front_pos = None
    match fac:
        case "^":
            front_pos = (pos[0], pos[1] - 1)
        case "v":
            front_pos = (pos[0], pos[1] + 1)
        case "<":
            front_pos = (pos[0] - 1, pos[1])
        case ">":
            front_pos = (pos[0] + 1, pos[1])
    if grid[front_pos] == "":
        return None
    else:
        return front_pos


def next_space(pos, fac, grid):
    next_pos = in_front(pos, fac, grid)
    if not next_pos:
        return None, fac
    if grid[next_pos] == "#":
        match fac:
            case "^":
                return pos, ">"
            case "v":
                return pos, "<"
            case "<":
                return pos, "^"
            case ">":
                return pos, "v"
    else:
        return next_pos, fac


def get_distinct_positions(grid, pos, fac):
    paths = []
    visits = [pos]
    while pos:
        prev_pos = pos
        pos, fac = next_space(pos, fac, grid)
        if (prev_pos, pos) in paths:
            return None
        if pos != prev_pos:
            paths.append((prev_pos, pos))
        if pos:
            visits.append(pos)
    return set(visits)


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
    pos = list(filter(lambda x: x[1] == "^", grid.items()))[0][0]
    fac = grid[pos]
    grid[pos] = "X"

    ##########
    # part 1 #
    ##########
    visits = get_distinct_positions(grid, pos, fac)
    print(len(visits))

    ##########
    # part 2 #
    ##########
    loop_locs = []
    for i, loc in enumerate(visits):
        print(i)
        grid[loc] = "#"
        if get_distinct_positions(grid, pos, fac) is None:
            loop_locs.append(loc)
        grid[loc] = "."
    print(len(loop_locs))


if __name__ == "__main__":
    main()
