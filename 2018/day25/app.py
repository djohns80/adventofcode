import os

MAX_LINK_DISTANCE = 3


def manhattan_distance(a, b):
    total = 0
    for a_coordinate, b_coordinate in zip(a, b):
        total += abs(a_coordinate - b_coordinate)
    return total


def count_constellations(points):
    """Count the groups of points that are chained together by links of at most MAX_LINK_DISTANCE."""
    unvisited = set(range(len(points)))
    constellations = 0
    while unvisited:
        # flood out from any point not yet in a constellation
        constellations += 1
        to_visit = [unvisited.pop()]
        while to_visit:
            current = points[to_visit.pop()]
            linked = []
            for index in unvisited:
                if manhattan_distance(current, points[index]) <= MAX_LINK_DISTANCE:
                    linked.append(index)
            for index in linked:
                unvisited.remove(index)
                to_visit.append(index)
    return constellations


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    points = []
    for line in lines:
        if not line.strip():
            continue
        coordinates = []
        for value in line.split(","):
            coordinates.append(int(value))
        points.append(tuple(coordinates))

    ##########
    # part 1 #
    ##########
    part_1 = count_constellations(points)
    print("part 1:", part_1)


if __name__ == "__main__":
    main()
