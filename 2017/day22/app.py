import os

BURSTS = 10000
EVOLVED_BURSTS = 10000000
CLEAN = "."
WEAKENED = "W"
INFECTED = "#"
FLAGGED = "F"

# Positions and directions are complex numbers: column + row * 1j, so moving
# up is -1j. Turning is then a multiplication of the direction.
UP = -1j
TURN_LEFT = -1j
TURN_RIGHT = 1j
NO_TURN = 1
REVERSE = -1

# for each node state: (how the carrier turns, the state the node changes to)
BASIC_RULES = {
    CLEAN: (TURN_LEFT, INFECTED),
    INFECTED: (TURN_RIGHT, CLEAN),
}
EVOLVED_RULES = {
    CLEAN: (TURN_LEFT, WEAKENED),
    WEAKENED: (NO_TURN, INFECTED),
    INFECTED: (TURN_RIGHT, FLAGGED),
    FLAGGED: (REVERSE, CLEAN),
}


def parse_map(lines):
    # only infected nodes are stored; any position missing from the dict is clean
    nodes = {}
    for row, line in enumerate(lines):
        for column, character in enumerate(line):
            if character == INFECTED:
                nodes[column + row * 1j] = INFECTED
    start = len(lines[0]) // 2 + (len(lines) // 2) * 1j
    return nodes, start


def count_infections(nodes, start, bursts, rules):
    nodes = dict(nodes)  # work on a copy so the caller's map is unchanged
    position = start
    direction = UP
    infections = 0
    for _ in range(bursts):
        turn, new_state = rules[nodes.get(position, CLEAN)]
        direction *= turn
        nodes[position] = new_state
        if new_state == INFECTED:
            infections += 1
        position += direction
    return infections


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    nodes, start = parse_map(lines)

    ##########
    # part 1 #
    ##########
    part_1 = count_infections(nodes, start, BURSTS, BASIC_RULES)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = count_infections(nodes, start, EVOLVED_BURSTS, EVOLVED_RULES)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
