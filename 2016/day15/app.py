import math
import os
import re

DISC_PATTERN = re.compile(
    r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)\."
)
NEW_DISC_POSITIONS = 11
NEW_DISC_START_POSITION = 0


def first_button_time(discs):
    # discs is a list of (disc_number, positions, start_position).
    # The capsule reaches disc n at time t + n, so we need
    # (start_position + t + disc_number) % positions == 0 for every disc.
    # Line the discs up one at a time: once the first few discs are aligned,
    # stepping by the lcm of their sizes keeps them aligned.
    time = 0
    step = 1
    for disc_number, positions, start_position in discs:
        while (start_position + time + disc_number) % positions != 0:
            time += step
        step = math.lcm(step, positions)
    return time


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    discs = []
    for line in lines:
        match = DISC_PATTERN.fullmatch(line.strip())
        disc_number, positions, start_position = match.groups()
        discs.append((int(disc_number), int(positions), int(start_position)))

    ##########
    # part 1 #
    ##########
    part_1 = first_button_time(discs)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # a new disc appears below all the others
    new_disc = (len(discs) + 1, NEW_DISC_POSITIONS, NEW_DISC_START_POSITION)
    part_2 = first_button_time(discs + [new_disc])
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
