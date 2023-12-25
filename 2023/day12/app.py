import os
from functools import lru_cache


@lru_cache(None)
def recursive_calc(springs, runs, sidx=0, ridx=0):
    if sidx != 0:
        assert sidx - 1 >= len(springs) or springs[sidx - 1] != "#"
    # try to match first run
    if ridx >= len(runs):
        if sidx <= len(springs) + 1:
            # ensure there's no leftovers
            if not any(c == "#" for c in springs[sidx:]):
                return 1
            return 0
        return 0
    run_to_match = runs[ridx]
    cidx = sidx
    o = 0
    # check if next run of # is too big
    while cidx <= len(springs) - run_to_match:
        if springs[cidx] == "#":
            if all(c in "#?" for c in springs[cidx : cidx + run_to_match]) and (
                cidx + run_to_match == len(springs)
                or springs[cidx + run_to_match] in ".?"
            ):
                o += recursive_calc(springs, runs, cidx + run_to_match + 1, ridx + 1)
            return o
        if all(c in "#" for c in springs[cidx : cidx + run_to_match]):
            # force break
            try:
                if springs[cidx + run_to_match] == "#":
                    return o
            finally:
                pass
            o += recursive_calc(springs, runs, cidx + run_to_match + 1, ridx + 1)
            break
        if (
            all(c in "#?" for c in springs[cidx : cidx + run_to_match])
            and (
                cidx + run_to_match == len(springs)
                or springs[cidx + run_to_match] in ".?"
            )
            and (cidx == 0 or springs[cidx - 1] in ".?")
        ):
            o += recursive_calc(springs, runs, cidx + run_to_match + 1, ridx + 1)
        cidx += 1
    return o


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.split, map(str.strip, file.readlines())))
    data = [[line[0], tuple(map(int, line[1].split(",")))] for line in lines]

    ##########
    # part 1 #
    ##########
    part_1 = 0
    for spring, run in data:
        part_1 += recursive_calc(tuple(spring), run)
    print(part_1)

    ##########
    # part 2 #
    ##########
    data_2 = [["?".join([d[0]] * 5), d[1] * 5] for d in data]
    part_2 = 0
    for spring, run in data_2:
        part_2 += recursive_calc(tuple(spring), run)
    print(part_2)


if __name__ == "__main__":
    main()
