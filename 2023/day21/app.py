import os
from collections import deque

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))
    grid = list(map(list, lines))
    rows = len(grid)
    cols = len(grid[0])
    start = [
        (y, x) for y, line in enumerate(grid) for x, c in enumerate(line) if c == "S"
    ][0]

    def print_grid():
        for line in grid:
            print("".join(line))

    def valid_steps(pos):
        output = []
        for d in directions:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if (
                0 <= new_pos[0] < rows
                and 0 <= new_pos[1] < cols
                and grid[new_pos[0]][new_pos[1]] == "."
            ):
                output.append(new_pos)
        return output

    ##########
    # part 1 #
    ##########
    steps = deque([(start, 0)])
    plots = {start}
    while len(steps) > 0:
        step, step_count = steps.pop()
        if step_count >= 64:
            plots.add(step)
            continue
        for v in valid_steps(step):
            steps.append((v, step_count + 1))

    print(len(plots))

    ##########
    # part 2 #
    ##########


if __name__ == "__main__":
    main()
