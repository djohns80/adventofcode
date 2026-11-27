import os

DOWN = (1, 0)


def cell(grid, row, column):
    # anything off the edge of the diagram counts as empty space
    if 0 <= row < len(grid) and 0 <= column < len(grid[row]):
        return grid[row][column]
    return " "


def turn(grid, row, column, direction):
    # at a "+" the only options are left or right of the current direction
    row_step, column_step = direction
    for new_direction in ((column_step, row_step), (-column_step, -row_step)):
        if cell(grid, row + new_direction[0], column + new_direction[1]) != " ":
            return new_direction
    raise ValueError(f"dead end at a corner: row {row}, column {column}")


def follow_path(grid):
    """Return the letters seen along the path and the number of steps taken."""
    row = 0
    column = grid[0].index("|")
    direction = DOWN
    letters = []
    steps = 0
    while cell(grid, row, column) != " ":
        current = cell(grid, row, column)
        if current.isalpha():
            letters.append(current)
        elif current == "+":
            direction = turn(grid, row, column, direction)
        row += direction[0]
        column += direction[1]
        steps += 1
    return "".join(letters), steps


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    # keep leading spaces: the column positions matter
    grid = content.splitlines()
    # one walk along the path answers both parts
    letters, steps = follow_path(grid)

    ##########
    # part 1 #
    ##########
    part_1 = letters
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = steps
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
