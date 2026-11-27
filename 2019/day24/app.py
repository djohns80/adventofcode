import os

GRID_SIZE = 5
MINUTES = 200

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def parse_bugs(lines):
    """Return the set of (row, col) tiles that contain a bug."""
    bugs = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                bugs.add((row, col))
    return bugs


def grid_neighbours(tile, grid_size):
    """The up to four adjacent (row, col) tiles that are inside the grid."""
    row, col = tile
    neighbours = []
    for d_row, d_col in DIRECTIONS:
        new_row = row + d_row
        new_col = col + d_col
        if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
            neighbours.append((new_row, new_col))
    return neighbours


def recursive_neighbours(tile, grid_size):
    """
    The adjacent (level, row, col) tiles in the recursive grids. The middle tile is
    the grid one level deeper (level + 1), and the grid sits inside the middle tile
    of the grid one level out (level - 1).
    """
    level, row, col = tile
    middle = grid_size // 2
    last = grid_size - 1
    neighbours = []
    for d_row, d_col in DIRECTIONS:
        new_row = row + d_row
        new_col = col + d_col
        if not (0 <= new_row < grid_size and 0 <= new_col < grid_size):
            # off the edge: the tile next to the middle in the grid one level out
            neighbours.append((level - 1, middle + d_row, middle + d_col))
        elif new_row == middle and new_col == middle:
            # into the middle: the whole facing edge of the grid one level deeper
            for i in range(grid_size):
                if d_row == 1:
                    neighbours.append((level + 1, 0, i))
                elif d_row == -1:
                    neighbours.append((level + 1, last, i))
                elif d_col == 1:
                    neighbours.append((level + 1, i, 0))
                else:
                    neighbours.append((level + 1, i, last))
        else:
            neighbours.append((level, new_row, new_col))
    return neighbours


def step(bugs, neighbours_of, grid_size):
    """Advance one minute. neighbours_of(tile, grid_size) gives the adjacent tiles."""
    # count adjacent bugs for every tile next to at least one bug
    adjacent_counts = {}
    for bug in bugs:
        for neighbour in neighbours_of(bug, grid_size):
            adjacent_counts[neighbour] = adjacent_counts.get(neighbour, 0) + 1

    new_bugs = set()
    for tile, count in adjacent_counts.items():
        if tile in bugs:
            if count == 1:
                new_bugs.add(tile)
        elif count == 1 or count == 2:
            new_bugs.add(tile)
    # bugs with no adjacent bugs aren't in adjacent_counts, and they die anyway
    return new_bugs


def first_repeated_layout(bugs, grid_size):
    """Step until a layout appears for the second time, and return it."""
    seen = set()
    layout = frozenset(bugs)
    while layout not in seen:
        seen.add(layout)
        layout = frozenset(step(layout, grid_neighbours, grid_size))
    return layout


def biodiversity(bugs, grid_size):
    """Each tile, in reading order, is worth increasing powers of two."""
    rating = 0
    for row, col in bugs:
        rating += 2 ** (row * grid_size + col)
    return rating


def bugs_after(bugs, minutes, neighbours_of, grid_size):
    """The bugs left after this many minutes."""
    for _ in range(minutes):
        bugs = step(bugs, neighbours_of, grid_size)
    return bugs


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    bugs = parse_bugs(lines)

    ##########
    # part 1 #
    ##########
    repeated = first_repeated_layout(bugs, GRID_SIZE)
    part_1 = biodiversity(repeated, GRID_SIZE)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # the scan is level 0, every other level starts empty
    recursive_bugs = set()
    for row, col in bugs:
        recursive_bugs.add((0, row, col))
    final_bugs = bugs_after(recursive_bugs, MINUTES, recursive_neighbours, GRID_SIZE)
    part_2 = len(final_bugs)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
