import heapq
import os

MOUTH = (0, 0)
X_MULTIPLIER = 16807
Y_MULTIPLIER = 48271
EROSION_MODULO = 20183
# region type is erosion level % 3, and each type's risk level is that same number
ROCKY = 0
WET = 1
NARROW = 2

TORCH = "torch"
CLIMBING_GEAR = "climbing gear"
NEITHER = "neither"
ALLOWED_TOOLS = {
    ROCKY: (CLIMBING_GEAR, TORCH),
    WET: (CLIMBING_GEAR, NEITHER),
    NARROW: (TORCH, NEITHER),
}
START_TOOL = TORCH
TARGET_TOOL = TORCH
MOVE_MINUTES = 1
SWITCH_MINUTES = 7
STEPS = ((0, -1), (0, 1), (-1, 0), (1, 0))
# how far past the target the map is first built; it is doubled if that turns out too small
INITIAL_MARGIN = 200


def erosion_levels(depth, target, width, height):
    """Erosion level of every region with x < width and y < height, as rows indexed [y][x]."""
    levels = []
    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) == MOUTH or (x, y) == target:
                geologic_index = 0
            elif y == 0:
                geologic_index = x * X_MULTIPLIER
            elif x == 0:
                geologic_index = y * Y_MULTIPLIER
            else:
                geologic_index = row[x - 1] * levels[y - 1][x]
            row.append((geologic_index + depth) % EROSION_MODULO)
        levels.append(row)
    return levels


def region_types(depth, target, width, height):
    """Type (ROCKY, WET or NARROW) of every region with x < width and y < height, as rows indexed [y][x]."""
    types = []
    for erosion_row in erosion_levels(depth, target, width, height):
        row = []
        for erosion_level in erosion_row:
            row.append(erosion_level % 3)
        types.append(row)
    return types


def total_risk_level(depth, target):
    """Sum of the risk levels in the rectangle from the mouth to the target."""
    target_x, target_y = target
    types = region_types(depth, target, target_x + 1, target_y + 1)
    total = 0
    for row in types:
        total += sum(row)
    return total


def fastest_time_within(types, target):
    """
    Dijkstra over (x, y, tool) states: fewest minutes from the mouth with START_TOOL
    to the target with TARGET_TOOL, without leaving the given grid of region types.
    """
    height = len(types)
    width = len(types[0])
    mouth_x, mouth_y = MOUTH
    target_state = (target[0], target[1], TARGET_TOOL)
    best_minutes = {(mouth_x, mouth_y, START_TOOL): 0}
    queue = [(0, mouth_x, mouth_y, START_TOOL)]
    while queue:
        minutes, x, y, tool = heapq.heappop(queue)
        if (x, y, tool) == target_state:
            return minutes
        if minutes > best_minutes[(x, y, tool)]:
            # a faster way to this state was already handled
            continue

        options = []
        # every region allows exactly two tools, so switching means taking the other one
        for other_tool in ALLOWED_TOOLS[types[y][x]]:
            if other_tool != tool:
                options.append((minutes + SWITCH_MINUTES, x, y, other_tool))
        for dx, dy in STEPS:
            next_x = x + dx
            next_y = y + dy
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue
            if tool in ALLOWED_TOOLS[types[next_y][next_x]]:
                options.append((minutes + MOVE_MINUTES, next_x, next_y, tool))

        for option in options:
            option_minutes, option_x, option_y, option_tool = option
            state = (option_x, option_y, option_tool)
            if state not in best_minutes or option_minutes < best_minutes[state]:
                best_minutes[state] = option_minutes
                heapq.heappush(queue, option)
    return None


def fastest_time(depth, target):
    """Fewest minutes to reach the target, building the map some way past the target."""
    target_x, target_y = target
    margin = INITIAL_MARGIN
    while True:
        width = target_x + 1 + margin
        height = target_y + 1 + margin
        types = region_types(depth, target, width, height)
        minutes = fastest_time_within(types, target)
        # A route that leaves the map has to go more than `margin` past the target in x or y
        # and then come back, so it takes at least this long. If the route found is no slower,
        # nothing beyond the edge could have beaten it.
        leaving_route_minimum = (target_x + target_y + 2 * (margin + 1)) * MOVE_MINUTES
        if minutes is not None and minutes <= leaving_route_minimum:
            return minutes
        margin *= 2


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    depth = int(lines[0].split(":")[1])
    target_x, target_y = lines[1].split(":")[1].split(",")
    target = (int(target_x), int(target_y))

    ##########
    # part 1 #
    ##########
    part_1 = total_risk_level(depth, target)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = fastest_time(depth, target)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
