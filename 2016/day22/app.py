import os
from collections import deque

TARGET_POSITION = (0, 0)  # the only node we can access directly


def count_viable_pairs(nodes):
    """Count ordered pairs (A, B) of different nodes where A's data fits in B's free space."""
    count = 0
    for position_a, node_a in nodes.items():
        if node_a["used"] == 0:
            continue
        for position_b, node_b in nodes.items():
            if position_a != position_b and node_a["used"] <= node_b["avail"]:
                count += 1
    return count


def fewest_steps_to_target(nodes, target_position):
    """Fewest moves to bring the data from the top-right node to the target node.

    This relies on the layout of the example and the real input (as part 1's
    viable pairs show):
    - there is exactly one empty node, and every viable move is into it, so a
      move is really "slide the empty node to a neighbour";
    - nodes holding more data than the empty node can store are walls that never move;
    - every other node's data fits in any other non-wall node, so they are interchangeable.
    The state is then just (where the empty node is, where the goal data is).
    """
    max_x = 0
    for x, _ in nodes:
        max_x = max(max_x, x)
    goal_start = (max_x, 0)

    empty_start = None
    for position, node in nodes.items():
        if node["used"] == 0:
            empty_start = position
    empty_size = nodes[empty_start]["size"]

    walls = set()
    for position, node in nodes.items():
        if node["used"] > empty_size:
            walls.add(position)

    start_state = (empty_start, goal_start)
    queue = deque([(start_state, 0)])
    seen = {start_state}
    while queue:
        (empty, goal), steps = queue.popleft()
        if goal == target_position:
            return steps
        x, y = empty
        for neighbour in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if neighbour not in nodes or neighbour in walls:
                continue
            # the neighbour's data moves into the empty node, leaving the neighbour empty
            new_goal = empty if neighbour == goal else goal
            state = (neighbour, new_goal)
            if state not in seen:
                seen.add(state)
                queue.append((state, steps + 1))
    return None


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    nodes = {}
    for line in lines:
        # skip the command and header lines at the top of the df output
        if not line.startswith("/dev/grid/"):
            continue
        name, size, used, avail, _ = line.split()
        _, x, y = name.split("-")
        position = (int(x[1:]), int(y[1:]))
        nodes[position] = {
            "size": int(size.rstrip("T")),
            "used": int(used.rstrip("T")),
            "avail": int(avail.rstrip("T")),
        }

    ##########
    # part 1 #
    ##########
    part_1 = count_viable_pairs(nodes)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = fewest_steps_to_target(nodes, TARGET_POSITION)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
