import os
import re


def positions_at(points, seconds):
    """Return the (x, y) position of every point after the given number of seconds."""
    positions = []
    for x, y, velocity_x, velocity_y in points:
        positions.append((x + velocity_x * seconds, y + velocity_y * seconds))
    return positions


def bounding_box(positions):
    """Return (min_x, min_y, max_x, max_y) of the positions."""
    xs = []
    ys = []
    for x, y in positions:
        xs.append(x)
        ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def bounding_box_area(positions):
    min_x, min_y, max_x, max_y = bounding_box(positions)
    return (max_x - min_x + 1) * (max_y - min_y + 1)


def find_message_time(points):
    """Return the second at which the points are packed most tightly together.

    The points converge, form the message, then spread out again, so we step
    forward until the bounding box starts growing.
    """
    seconds = 0
    area = bounding_box_area(positions_at(points, seconds))
    while True:
        next_area = bounding_box_area(positions_at(points, seconds + 1))
        if next_area > area:
            return seconds
        seconds += 1
        area = next_area


def draw(positions):
    """Return the positions drawn as rows of "#" (point) and "." (empty sky)."""
    min_x, min_y, max_x, max_y = bounding_box(positions)
    lit = set(positions)
    rows = []
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in lit:
                row += "#"
            else:
                row += "."
        rows.append(row)
    return "\n".join(rows)


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
        # "position=< 9,  1> velocity=< 0,  2>" -> (9, 1, 0, 2)
        x, y, velocity_x, velocity_y = re.findall(r"-?\d+", line)
        points.append((int(x), int(y), int(velocity_x), int(velocity_y)))

    ##########
    # part 1 #
    ##########
    message_time = find_message_time(points)
    part_1 = draw(positions_at(points, message_time))
    print("part 1:")
    print(part_1)

    ##########
    # part 2 #
    ##########
    part_2 = message_time
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
