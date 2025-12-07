import os
from collections import defaultdict


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = [list(line.strip()) for line in content.splitlines()]
    width = len(lines[0])

    ##########
    # part 1 #
    ##########
    beams = ["|" if v == "S" else v for v in lines[0]]
    part_1 = 0
    for row in lines[1:]:
        for pos, cell in enumerate(row):
            if beams[pos] == "|":
                if cell == "^":
                    part_1 += 1
                    beams[pos] = "."
                    for new_pos in [pos - 1, pos + 1]:
                        if 0 <= new_pos < width:
                            beams[new_pos] = "|"
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    particles = defaultdict(int)
    particles[lines[0].index("S")] = 1
    for line in lines[1:]:
        new_particles = defaultdict(int)
        for pos, count in particles.items():
            if line[pos] == ".":
                new_particles[pos] += count
            elif line[pos] == "^":
                for new_pos in [pos - 1, pos + 1]:
                    if 0 <= new_pos < width:
                        new_particles[new_pos] += count
        particles = new_particles
    part_2 = sum(particles.values())
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
