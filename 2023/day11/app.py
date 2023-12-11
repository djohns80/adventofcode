import os


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))
    galaxies = []
    for y, line in enumerate(lines):
        for x, c in enumerate(list(line)):
            if c == "#":
                galaxies.append((y, x))

    blank_rows = [i for i in range(len(lines)) if "#" not in lines[i]]
    blank_columns = [
        i for i in range(len(lines[0])) if "#" not in [line[i] for line in lines]
    ]

    def expand_galaxies(n):
        expanded_galaxies = []
        for y, x in galaxies:
            y += sum([1 for r in blank_rows if y > r]) * (n - 1)
            x += sum([1 for c in blank_columns if x > c]) * (n - 1)
            expanded_galaxies.append((y, x))
        return expanded_galaxies

    def get_shortest_paths(positions):
        pair_galaxies = [
            (positions[a], positions[b])
            for a in range(len(positions))
            for b in range(a, len(positions))
            if a != b
        ]
        return [abs(p[0][0] - p[1][0]) + abs(p[0][1] - p[1][1]) for p in pair_galaxies]

    ##########
    # part 1 #
    ##########
    print(sum(get_shortest_paths(expand_galaxies(2))))

    ##########
    # part 2 #
    ##########
    print(sum(get_shortest_paths(expand_galaxies(1000000))))


if __name__ == "__main__":
    main()
