import os


def parse_programs(lines):
    """Return {name: (weight, [names of programs held up on its disc])}."""
    programs = {}
    for line in lines:
        if not line.strip():
            continue
        if " -> " in line:
            program_part, held_part = line.split(" -> ")
            held = held_part.split(", ")
        else:
            program_part = line
            held = []
        name, weight_part = program_part.split()
        programs[name] = (int(weight_part.strip("()")), held)
    return programs


def find_bottom_program(programs):
    # the bottom program is the only one that no other program holds up
    held_programs = set()
    for _, held in programs.values():
        for name in held:
            held_programs.add(name)
    for name in programs:
        if name not in held_programs:
            return name
    return None


def tower_weight(programs, name):
    """Weight of a program plus every program above it."""
    weight, held = programs[name]
    total = weight
    for child in held:
        total += tower_weight(programs, child)
    return total


def find_corrected_weight(programs, bottom):
    """Return the weight the one wrongly weighted program needs to balance the tower."""
    name = bottom
    target_tower_weight = None
    while True:
        _, held = programs[name]
        child_weights = {}
        weight_counts = {}
        for child in held:
            weight = tower_weight(programs, child)
            child_weights[child] = weight
            weight_counts[weight] = weight_counts.get(weight, 0) + 1

        odd_child = None
        balanced_weight = None
        for child, weight in child_weights.items():
            if weight_counts[weight] == 1 and len(held) > 2:
                odd_child = child
            else:
                balanced_weight = weight

        if odd_child is None:
            # everything above this program is balanced, so its own weight is
            # wrong: shift it by however much its tower is off the target
            own_weight, _ = programs[name]
            return own_weight + target_tower_weight - tower_weight(programs, name)

        # climb into the sub-tower that doesn't match its siblings
        name = odd_child
        target_tower_weight = balanced_weight


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    programs = parse_programs(lines)

    ##########
    # part 1 #
    ##########
    part_1 = find_bottom_program(programs)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = find_corrected_weight(programs, part_1)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
