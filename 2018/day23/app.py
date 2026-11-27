import heapq
import os
import re
from itertools import product

ORIGIN = (0, 0, 0)


def manhattan_distance(a, b):
    total = 0
    for a_coordinate, b_coordinate in zip(a, b):
        total += abs(a_coordinate - b_coordinate)
    return total


def in_range_of_strongest(nanobots):
    """Count the nanobots (including itself) within range of the one with the largest radius."""
    strongest_position, strongest_radius = max(nanobots, key=lambda bot: bot[1])
    count = 0
    for position, _ in nanobots:
        if manhattan_distance(strongest_position, position) <= strongest_radius:
            count += 1
    return count


def distance_to_cube(point, corner, size):
    """Manhattan distance from a point to the nearest point of the cube with this lowest corner and side length."""
    total = 0
    for coordinate, low in zip(point, corner):
        high = low + size - 1
        if coordinate < low:
            total += low - coordinate
        elif coordinate > high:
            total += coordinate - high
    return total


def bots_reaching_cube(nanobots, corner, size):
    """How many nanobots have at least one point of the cube in range."""
    count = 0
    for position, radius in nanobots:
        if distance_to_cube(position, corner, size) <= radius:
            count += 1
    return count


def best_position_distance(nanobots):
    """
    Distance from ORIGIN to the nearest point that is in range of the most nanobots.

    Best-first search over cubes. A cube's score is how many bots can reach at least one point
    in it, which is an upper bound for every point inside it. The queue always gives back the
    cube with the highest score, then the one nearest the origin, then the smallest, and that
    cube is split into 8 halves (whose scores can only be lower and distances only larger).
    So the first single point to come out can't be beaten by anything still queued: nothing
    there scores higher, and nothing that scores the same is nearer.
    """
    # The best point is in range of at least one bot, so start with a cube covering every
    # bot's whole range. Its side is a power of two so it splits evenly down to single points.
    low = None
    high = None
    for position, radius in nanobots:
        for coordinate in position:
            if low is None or coordinate - radius < low:
                low = coordinate - radius
            if high is None or coordinate + radius > high:
                high = coordinate + radius
    size = 1
    while low + size - 1 < high:
        size *= 2
    corner = (low, low, low)

    # queue entries: (-score, distance from origin, side length, lowest corner)
    queue = [
        (
            -bots_reaching_cube(nanobots, corner, size),
            distance_to_cube(ORIGIN, corner, size),
            size,
            corner,
        )
    ]
    while queue:
        _, distance, size, corner = heapq.heappop(queue)
        if size == 1:
            return distance
        half = size // 2
        # the 8 sub-cubes: each axis either keeps the low half or moves to the high half
        for offset in product((0, half), repeat=3):
            sub_corner = (
                corner[0] + offset[0],
                corner[1] + offset[1],
                corner[2] + offset[2],
            )
            heapq.heappush(
                queue,
                (
                    -bots_reaching_cube(nanobots, sub_corner, half),
                    distance_to_cube(ORIGIN, sub_corner, half),
                    half,
                    sub_corner,
                ),
            )
    return None


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    nanobots = []
    for line in lines:
        x, y, z, radius = map(int, re.findall(r"-?\d+", line))
        nanobots.append(((x, y, z), radius))

    ##########
    # part 1 #
    ##########
    part_1 = in_range_of_strongest(nanobots)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = best_position_distance(nanobots)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
