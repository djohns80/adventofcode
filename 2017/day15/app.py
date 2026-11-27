import os
from itertools import islice

FACTOR_A = 16807
FACTOR_B = 48271
DIVISOR = 2147483647
LOW_16_BITS = 0xFFFF
PAIRS_TO_CHECK = 40_000_000
PICKY_MULTIPLE_A = 4
PICKY_MULTIPLE_B = 8
PICKY_PAIRS_TO_CHECK = 5_000_000


def generator(start, factor, multiple=1):
    # only values that are a multiple of `multiple` are handed to the judge
    value = start
    while True:
        value = value * factor % DIVISOR
        if value % multiple == 0:
            yield value


def judge_count(start_a, start_b, pairs, multiple_a=1, multiple_b=1):
    # tens of millions of values per part is inherently slow in pure Python
    # (around 30-40 s for both parts), so this loop is kept as lean as possible
    generator_a = generator(start_a, FACTOR_A, multiple_a)
    generator_b = generator(start_b, FACTOR_B, multiple_b)
    matches = 0
    for value_a, value_b in islice(zip(generator_a, generator_b), pairs):
        if value_a & LOW_16_BITS == value_b & LOW_16_BITS:
            matches += 1
    return matches


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    # each line looks like "Generator A starts with 722"
    starts = {}
    for line in lines:
        words = line.split()
        starts[words[1]] = int(words[-1])

    ##########
    # part 1 #
    ##########
    part_1 = judge_count(starts["A"], starts["B"], PAIRS_TO_CHECK)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = judge_count(
        starts["A"],
        starts["B"],
        PICKY_PAIRS_TO_CHECK,
        PICKY_MULTIPLE_A,
        PICKY_MULTIPLE_B,
    )
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
