import os
from itertools import combinations
from math import prod


def get_qe(weights, group_count):
    target_weight = sum(weights) // group_count
    for group_size in range(1, len(weights) + 1):
        groups = [
            g for g in combinations(weights, group_size) if sum(g) == target_weight
        ]
        if groups:
            break
    return min(map(prod, groups))


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    weights = [int(w) for w in lines]

    ##########
    # part 1 #
    ##########
    print("part 1:", get_qe(weights, 3))

    ##########
    # part 2 #
    ##########
    print("part 2:", get_qe(weights, 4))


if __name__ == "__main__":
    main()
