import os

SPRING = (500, 0)


def parse_clay(lines):
    # each line is a vertical or horizontal vein, e.g. "x=495, y=2..7"
    clay = set()
    for line in lines:
        fixed_part, range_part = line.split(", ")
        fixed_axis, fixed_value = fixed_part.split("=")
        range_start, range_end = range_part[2:].split("..")
        for value in range(int(range_start), int(range_end) + 1):
            if fixed_axis == "x":
                clay.add((int(fixed_value), value))
            else:
                clay.add((value, int(fixed_value)))
    return clay


def y_range(clay):
    clay_ys = []
    for _, y in clay:
        clay_ys.append(y)
    return min(clay_ys), max(clay_ys)


def scan_row(x, y, step, clay, settled):
    # walk sideways from x (step is -1 or 1) for as long as the tile underneath
    # can hold water up; returns where the walk stopped and whether that was
    # because of a clay wall (otherwise the water falls from that tile)
    while (x, y + 1) in clay or (x, y + 1) in settled:
        if (x + step, y) in clay:
            return x, True
        x += step
    return x, False


def simulate_water(clay, spring):
    # returns the tiles water flows through and the tiles where it settles
    _, max_y = y_range(clay)
    flowing = set()
    settled = set()
    # An explicit stack rather than recursion (the real input is too deep).
    # Whenever a tile adds new tiles to explore, it is pushed back underneath
    # them, so it gets looked at again once the water below has been worked out
    # (e.g. a reservoir below may have filled up to just beneath it).
    stack = [spring]
    while stack:
        x, y = stack.pop()
        if (x, y) in settled:
            continue
        below = (x, y + 1)
        if y + 1 > max_y or below in flowing:
            # falls off the bottom of the scan, or joins water that drains away
            continue
        if below not in clay and below not in settled:
            # sand underneath, so keep falling
            flowing.add(below)
            stack.append((x, y))
            stack.append(below)
            continue

        # something solid underneath, so spread out sideways along this row
        left_x, left_wall = scan_row(x, y, -1, clay, settled)
        right_x, right_wall = scan_row(x, y, 1, clay, settled)
        row = []
        for row_x in range(left_x, right_x + 1):
            row.append((row_x, y))
        if left_wall and right_wall:
            # walls on both sides: the whole row settles
            for tile in row:
                settled.add(tile)
                flowing.discard(tile)
            continue
        for tile in row:
            flowing.add(tile)
        # open ends with untouched sand below still need to be followed down
        falling_ends = []
        if not left_wall and (left_x, y + 1) not in flowing:
            falling_ends.append((left_x, y))
        if not right_wall and (right_x, y + 1) not in flowing:
            falling_ends.append((right_x, y))
        if falling_ends:
            stack.append((x, y))
            stack.extend(falling_ends)
    return flowing, settled


def count_tiles_in_range(tiles, min_y, max_y):
    count = 0
    for _, y in tiles:
        if min_y <= y <= max_y:
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
    clay = parse_clay(lines)
    min_y, max_y = y_range(clay)

    ##########
    # part 1 #
    ##########
    flowing, settled = simulate_water(clay, SPRING)
    part_1 = count_tiles_in_range(flowing | settled, min_y, max_y)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # only the settled water stays once the spring runs dry
    part_2 = count_tiles_in_range(settled, min_y, max_y)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
