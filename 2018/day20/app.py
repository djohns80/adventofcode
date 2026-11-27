import os
from collections import deque

START = (0, 0)
DIRECTIONS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}
MIN_DOORS = 1000


def build_map(regex):
    """Follow every route in the regex and return a dict of room -> set of rooms it has a door to."""
    doors = {START: set()}
    # all the rooms the routes followed so far could currently be in
    current = {START}
    # one entry per open "(": the rooms the group started from, and the rooms its finished options ended in
    branches = []
    for char in regex:
        if char in DIRECTIONS:
            dx, dy = DIRECTIONS[char]
            moved = set()
            for x, y in current:
                next_room = (x + dx, y + dy)
                doors[(x, y)].add(next_room)
                doors.setdefault(next_room, set()).add((x, y))
                moved.add(next_room)
            current = moved
        elif char == "(":
            branches.append((current, set()))
        elif char == "|":
            group_starts, group_ends = branches[-1]
            group_ends.update(current)
            current = group_starts
        elif char == ")":
            group_starts, group_ends = branches.pop()
            group_ends.update(current)
            current = group_ends
        # "^" and "$" just mark the start and end of the regex
    return doors


def room_distances(doors, start):
    """Breadth-first search: fewest doors needed to reach each room from start."""
    distances = {start: 0}
    queue = deque([start])
    while queue:
        room = queue.popleft()
        for neighbour in doors[room]:
            if neighbour not in distances:
                distances[neighbour] = distances[room] + 1
                queue.append(neighbour)
    return distances


def count_rooms_at_least(distances, min_doors):
    """Count the rooms whose shortest path passes through at least min_doors doors."""
    count = 0
    for doors_passed in distances.values():
        if doors_passed >= min_doors:
            count += 1
    return count


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    regex = lines[0]
    doors = build_map(regex)
    distances = room_distances(doors, START)

    ##########
    # part 1 #
    ##########
    part_1 = max(distances.values())
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = count_rooms_at_least(distances, MIN_DOORS)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
