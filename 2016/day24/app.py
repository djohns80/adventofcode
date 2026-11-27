import os
from collections import deque
from itertools import pairwise, permutations

START_LOCATION = 0


def parse_map(lines):
    """Return the set of open cells and {location number: (x, y)}."""
    open_cells = set()
    locations = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                continue
            open_cells.add((x, y))
            if char.isdigit():
                locations[int(char)] = (x, y)
    return open_cells, locations


def distances_from(start, open_cells):
    distances = {start: 0}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for neighbour in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if neighbour in open_cells and neighbour not in distances:
                distances[neighbour] = distances[(x, y)] + 1
                queue.append(neighbour)
    return distances


def location_distances(open_cells, locations):
    """Return {(location a, location b): fewest steps between them}."""
    pair_distances = {}
    for number, position in locations.items():
        distances = distances_from(position, open_cells)
        for other_number, other_position in locations.items():
            pair_distances[(number, other_number)] = distances[other_position]
    return pair_distances


def fewest_steps(open_cells, locations, return_to_start=False):
    pair_distances = location_distances(open_cells, locations)
    to_visit = []
    for number in locations:
        if number != START_LOCATION:
            to_visit.append(number)

    best = None
    for order in permutations(to_visit):
        route = (START_LOCATION, *order)
        if return_to_start:
            route = (*route, START_LOCATION)
        steps = 0
        for current, following in pairwise(route):
            steps += pair_distances[(current, following)]
        if best is None or steps < best:
            best = steps
    return best


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    open_cells, locations = parse_map(lines)

    ##########
    # part 1 #
    ##########
    part_1 = fewest_steps(open_cells, locations)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = fewest_steps(open_cells, locations, return_to_start=True)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
