import os

directions = [
    -1 - 1j,
    0 - 1j,
    1 - 1j,
    -1 + 0j,
    1 + 0j,
    -1 + 1j,
    0 + 1j,
    1 + 1j,
]


def get_removable_rolls(grid):
    removable = set()
    for pos, obj in grid.items():
        if obj == "@":
            roll_count = 0
            for d in directions:
                pos_check = pos + d
                if pos_check in grid:
                    if grid[pos_check] == "@":
                        roll_count += 1
            if roll_count < 4:
                removable.add(pos)
    return removable


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = [line.strip() for line in content.splitlines()]
    grid = {x + y * 1j: c for y, line in enumerate(lines) for x, c in enumerate(line)}

    ##########
    # part 1 #
    ##########
    part_1 = get_removable_rolls(grid)
    print("part 1:", len(part_1))

    ##########
    # part 2 #
    ##########
    removals = get_removable_rolls(grid)
    part_2 = len(removals)
    while len(removals) > 0:
        for r in removals:
            grid[r] = "x"
        removals = get_removable_rolls(grid)
        part_2 += len(removals)
    print("part 1:", part_2)


if __name__ == "__main__":
    main()
