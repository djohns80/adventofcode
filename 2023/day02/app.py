import os
import re
import math
from collections import defaultdict


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = [line.strip() for line in file.readlines()]

    games = {}
    for line in lines:
        game_id = int(re.findall(r"^Game\s(?P<id>\d+)", line)[0])
        reveals = [
            {r.split()[1]: int(r.split()[0])}
            for r in re.findall(r"\d+\s(?:blue|green|red)", line)
        ]
        games[game_id] = reveals

    ##########
    # part 1 #
    ##########
    bag = {"red": 12, "green": 13, "blue": 14}
    part_1 = 0
    for game_id, reveals in games.items():
        possible = all([n <= bag[c] for r in reveals for c, n in r.items()])
        if possible:
            part_1 += game_id
    print(part_1)

    ##########
    # part 2 #
    ##########
    part_2 = 0
    for game_id, reveals in games.items():
        max_cubes = defaultdict(int)
        for c, n in [(c, n) for r in reveals for c, n in r.items()]:
            if n > max_cubes[c]:
                max_cubes[c] = n
        part_2 += math.prod(max_cubes.values())
    print(part_2)


if __name__ == "__main__":
    main()
