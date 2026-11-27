import os

# axial hex coordinates (q, r): q increases to the east, r increases to the south
DIRECTION_OFFSETS = {
    "n": (0, -1),
    "ne": (1, -1),
    "se": (1, 0),
    "s": (0, 1),
    "sw": (-1, 1),
    "nw": (-1, 0),
}


def hex_distance(position):
    """Fewest steps from the starting hex (0, 0) to position."""
    q, r = position
    return (abs(q) + abs(r) + abs(q + r)) // 2


def follow_path(directions):
    """Take each step in directions from the starting hex (0, 0).

    Returns the hex reached and the furthest distance from the start along the way.
    """
    q, r = 0, 0
    furthest_distance = 0
    for direction in directions:
        offset_q, offset_r = DIRECTION_OFFSETS[direction]
        q += offset_q
        r += offset_r
        furthest_distance = max(furthest_distance, hex_distance((q, r)))
    return (q, r), furthest_distance


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    directions = content.strip().split(",")
    final_position, furthest_distance = follow_path(directions)

    ##########
    # part 1 #
    ##########
    part_1 = hex_distance(final_position)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = furthest_distance
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
