import os
from collections import defaultdict


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = content.splitlines()
    row_count = len(lines)
    col_count = len(lines[0])
    antennae = defaultdict(list)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                antennae[char].append(x + y * 1j)

    antinodes_1 = []
    antinodes_2 = []
    # Add antinodes (for part 2 only) where the antenna are with at least 2 of same freq.
    for locs in antennae.values():
        if len(locs) > 2:
            antinodes_2.extend(locs)
    for locs in antennae.values():
        for i, loc1 in enumerate(locs):
            for loc2 in locs[i + 1 :]:
                vec = loc1 - loc2
                for loc, diff in [(loc1, vec), (loc2, -vec)]:
                    antinode = loc + diff
                    if antinode.real >= 0 and antinode.real < col_count and antinode.imag >= 0 and antinode.imag < row_count:
                        antinodes_1.append(antinode)
                    while antinode.real >= 0 and antinode.real < col_count and antinode.imag >= 0 and antinode.imag < row_count:
                        antinodes_2.append(antinode)
                        antinode += diff


    ##########
    # part 1 #
    ##########
    print(len(set(antinodes_1)))

    ##########
    # part 2 #
    ##########
    print(len(set(antinodes_2)))


if __name__ == "__main__":
    main()
