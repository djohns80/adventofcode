import os
from collections import deque

START = (1, 1)
TARGET = (31, 39)
MAX_STEPS = 50


def is_open(x, y, favourite_number):
    value = x * x + 3 * x + 2 * x * y + y + y * y + favourite_number
    return value.bit_count() % 2 == 0


def explore(favourite_number, target=None, max_steps=None):
    """BFS from START.

    With a target, return the fewest steps to reach it. With max_steps, return
    how many distinct locations (including START) are reachable in that many steps.
    """
    queue = deque([(START, 0)])
    seen = {START}
    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == target:
            return steps
        if steps == max_steps:
            continue
        for neighbour in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            new_x, new_y = neighbour
            if new_x < 0 or new_y < 0 or neighbour in seen:
                continue
            if not is_open(new_x, new_y, favourite_number):
                continue
            seen.add(neighbour)
            queue.append((neighbour, steps + 1))
    if target is not None:
        return None
    return len(seen)


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    favourite_number = int(lines[0])

    ##########
    # part 1 #
    ##########
    part_1 = explore(favourite_number, target=TARGET)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = explore(favourite_number, max_steps=MAX_STEPS)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
