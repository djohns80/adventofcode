import heapq
import os
from collections import deque

WALL = "#"
ENTRANCE = "@"
# the 3x3 area around the single entrance is replaced by this to make four vaults
SPLIT_CENTRE = ("@#@", "###", "@#@")


def parse_vault(lines):
    """Return {(x, y): char} for every non-wall cell, and the entrance positions."""
    open_cells = {}
    entrances = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == WALL:
                continue
            open_cells[(x, y)] = char
            if char == ENTRANCE:
                entrances.append((x, y))
    return open_cells, entrances


def split_vault(lines):
    """Return the map with the area around the entrance replaced by SPLIT_CENTRE."""
    new_lines = list(lines)
    for y, line in enumerate(lines):
        x = line.find(ENTRANCE)
        if x == -1:
            continue
        for offset, replacement in enumerate(SPLIT_CENTRE):
            row = new_lines[y - 1 + offset]
            new_lines[y - 1 + offset] = row[: x - 1] + replacement + row[x + 2 :]
    return new_lines


def key_bit(letter):
    """Bit for a key, used for both the key ('a') and its door ('A')."""
    return 1 << (ord(letter.lower()) - ord("a"))


def reachable_keys(open_cells, origin):
    """BFS from origin to every key, ignoring doors.

    Returns a list of (key position, key bit, distance, keys needed), where keys
    needed covers the doors on the way and any other keys passed on the way.
    If a key is passed on the way, it's never worse to collect that key first,
    so requiring it keeps the search smaller without losing any answers.
    """
    results = []
    visited = {origin}
    queue = deque([(origin, 0, 0)])
    while queue:
        position, distance, needed = queue.popleft()
        char = open_cells[position]
        if char.isalpha() and position != origin:
            if char.islower():
                results.append((position, key_bit(char), distance, needed))
            needed |= key_bit(char)
        x, y = position
        for neighbour in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if neighbour in open_cells and neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, distance + 1, needed))
    return results


def fewest_steps(open_cells, entrances):
    """Return the fewest total steps for robots at the entrances to collect every key."""
    all_keys = 0
    origins = list(entrances)
    for position, char in open_cells.items():
        if char.islower():
            all_keys |= key_bit(char)
            origins.append(position)

    routes = {}
    for origin in origins:
        routes[origin] = reachable_keys(open_cells, origin)

    # Dijkstra over (robot positions, keys held as a bitmask)
    start_robots = tuple(entrances)
    best_steps = {(start_robots, 0): 0}
    queue = [(0, start_robots, 0)]
    while queue:
        steps, robots, held = heapq.heappop(queue)
        if held == all_keys:
            return steps
        if steps > best_steps[(robots, held)]:
            continue
        for robot_index, robot_position in enumerate(robots):
            for key_position, bit, distance, needed in routes[robot_position]:
                if held & bit:
                    continue  # already collected
                if needed & ~held:
                    continue  # a locked door or uncollected key is in the way
                new_robots = (
                    robots[:robot_index] + (key_position,) + robots[robot_index + 1 :]
                )
                new_held = held | bit
                new_steps = steps + distance
                state = (new_robots, new_held)
                if state not in best_steps or new_steps < best_steps[state]:
                    best_steps[state] = new_steps
                    heapq.heappush(queue, (new_steps, new_robots, new_held))
    return None


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    open_cells, entrances = parse_vault(lines)

    ##########
    # part 1 #
    ##########
    part_1 = fewest_steps(open_cells, entrances)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    open_cells, entrances = parse_vault(split_vault(lines))
    part_2 = fewest_steps(open_cells, entrances)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
