import math
import os

BET_POSITION = 200
X_MULTIPLIER = 100


def parse_asteroids(lines):
    """Return the (x, y) position of every asteroid on the map."""
    asteroids = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                asteroids.append((x, y))
    return asteroids


def group_by_direction(station, asteroids):
    """Return {direction: [asteroids]} for every other asteroid seen from station.

    The direction is the offset reduced by its greatest common divisor, so all
    asteroids on the same line of sight share a direction and only the nearest
    one in each group can be detected.
    """
    groups = {}
    for asteroid in asteroids:
        if asteroid == station:
            continue
        dx = asteroid[0] - station[0]
        dy = asteroid[1] - station[1]
        divisor = math.gcd(dx, dy)
        direction = (dx // divisor, dy // divisor)
        if direction not in groups:
            groups[direction] = []
        groups[direction].append(asteroid)
    return groups


def best_station(asteroids):
    """Return the asteroid that detects the most others, and how many it detects."""
    best_location = None
    best_count = -1
    for station in asteroids:
        detected = len(group_by_direction(station, asteroids))
        if detected > best_count:
            best_location = station
            best_count = detected
    return best_location, best_count


def clockwise_angle(direction):
    """Angle of a direction measured clockwise from straight up (y grows downwards)."""
    dx, dy = direction
    return math.atan2(dx, -dy) % (2 * math.pi)


def vaporisation_order(station, asteroids):
    """Return every other asteroid in the order the rotating laser vaporises them."""
    groups = group_by_direction(station, asteroids)
    directions = sorted(groups, key=clockwise_angle)
    for direction in directions:
        # nearest first; along one direction the Manhattan distance orders them
        groups[direction].sort(
            key=lambda asteroid: (
                abs(asteroid[0] - station[0]) + abs(asteroid[1] - station[1])
            )
        )

    # each rotation hits the nearest remaining asteroid in every direction
    order = []
    while len(order) < len(asteroids) - 1:
        for direction in directions:
            if groups[direction]:
                order.append(groups[direction].pop(0))
    return order


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    asteroids = parse_asteroids(lines)

    ##########
    # part 1 #
    ##########
    station, part_1 = best_station(asteroids)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    x, y = vaporisation_order(station, asteroids)[BET_POSITION - 1]
    part_2 = x * X_MULTIPLIER + y
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
