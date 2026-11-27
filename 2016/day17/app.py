import hashlib
import os
from collections import deque

GRID_SIZE = 4
START = (0, 0)
VAULT = (3, 3)
OPEN_DOOR_CHARS = "bcdef"

# the first four hash characters describe the doors in this order
DIRECTIONS = (("U", 0, -1), ("D", 0, 1), ("L", -1, 0), ("R", 1, 0))


def find_path(passcode, longest=False):
    # the path taken is part of the state (it changes which doors are open),
    # so there is no visited set; BFS finds paths in order of length, so the
    # first path to the vault is the shortest and the last one is the longest
    longest_path = None
    queue = deque([(START, "")])
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == VAULT:
            if not longest:
                return path
            # reaching the vault ends the path, so don't explore beyond it
            longest_path = path
            continue
        digest = hashlib.md5((passcode + path).encode()).hexdigest()
        for (letter, dx, dy), door in zip(DIRECTIONS, digest):
            new_x, new_y = x + dx, y + dy
            if door not in OPEN_DOOR_CHARS:
                continue
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                queue.append(((new_x, new_y), path + letter))
    return longest_path


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    passcode = lines[0].strip()

    ##########
    # part 1 #
    ##########
    part_1 = find_path(passcode)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = len(find_path(passcode, longest=True))
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
