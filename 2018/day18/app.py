import os

OPEN = "."
TREES = "|"
LUMBERYARD = "#"
MINUTES = 10
MINUTES_PART_2 = 1_000_000_000
GROWTH_THRESHOLD = 3  # adjacent trees/lumberyards needed for an acre to change


def count_neighbours(grid, row, col):
    """Count each kind of acre among the (up to) eight neighbours of an acre."""
    counts = {OPEN: 0, TREES: 0, LUMBERYARD: 0}
    for d_row in (-1, 0, 1):
        for d_col in (-1, 0, 1):
            if d_row == 0 and d_col == 0:
                continue
            r = row + d_row
            c = col + d_col
            if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
                counts[grid[r][c]] += 1
    return counts


def next_minute(grid):
    """Return the landscape after one minute; every acre changes simultaneously."""
    new_grid = []
    for row in range(len(grid)):
        new_row = []
        for col in range(len(grid[row])):
            acre = grid[row][col]
            counts = count_neighbours(grid, row, col)
            if acre == OPEN and counts[TREES] >= GROWTH_THRESHOLD:
                acre = TREES
            elif acre == TREES and counts[LUMBERYARD] >= GROWTH_THRESHOLD:
                acre = LUMBERYARD
            elif acre == LUMBERYARD and (counts[LUMBERYARD] == 0 or counts[TREES] == 0):
                acre = OPEN
            new_row.append(acre)
        new_grid.append(new_row)
    return new_grid


def resource_value(grid):
    wooded = 0
    lumberyards = 0
    for row in grid:
        wooded += row.count(TREES)
        lumberyards += row.count(LUMBERYARD)
    return wooded * lumberyards


def simulate(grid, minutes):
    """
    Return the landscape after the given number of minutes.
    The landscape eventually settles into a repeating loop, so as soon as a
    state repeats we can work out which earlier state the final minute matches
    instead of simulating all the way there (part 2 asks for a billion minutes).
    """
    history = []  # history[m] is the landscape after m minutes
    first_seen = {}  # landscape (as text) -> minute it first appeared
    for minute in range(minutes):
        state = ""
        for row in grid:
            state += "".join(row)
        if state in first_seen:
            loop_start = first_seen[state]
            loop_length = minute - loop_start
            return history[loop_start + (minutes - loop_start) % loop_length]
        first_seen[state] = minute
        history.append(grid)
        grid = next_minute(grid)
    return grid


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    grid = []
    for line in lines:
        grid.append(list(line))

    ##########
    # part 1 #
    ##########
    part_1 = resource_value(simulate(grid, MINUTES))
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = resource_value(simulate(grid, MINUTES_PART_2))
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
