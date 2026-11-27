import os

GENERATIONS = 20
MANY_GENERATIONS = 50_000_000_000


def next_generation(plants, growing_patterns):
    """Return the set of pots holding plants in the next generation.

    plants is the set of pot numbers that currently hold a plant, and
    growing_patterns is the set of "LLCRR" patterns that produce a plant.
    """
    new_plants = set()
    # Only pots within two of an existing plant can see a plant in their pattern.
    for pot in range(min(plants) - 2, max(plants) + 3):
        pattern = ""
        for neighbour in range(pot - 2, pot + 3):
            if neighbour in plants:
                pattern += "#"
            else:
                pattern += "."
        if pattern in growing_patterns:
            new_plants.add(pot)
    return new_plants


def shift_plants(plants, offset):
    """Return the plants moved offset pots to the right."""
    shifted = set()
    for pot in plants:
        shifted.add(pot + offset)
    return shifted


def simulate(plants, growing_patterns, generations):
    """Return the set of pots holding plants after the given number of generations.

    Eventually the plants settle into a fixed pattern that just slides along the
    row by the same number of pots every generation. The rules only look at
    neighbouring pots, never at pot numbers, so once a generation is an exact
    shifted copy of the one before, every later generation will be too. At that
    point we skip ahead by sliding the plants for all the remaining generations
    in one go, which makes a huge generation count instant.
    """
    for generation in range(generations):
        new_plants = next_generation(plants, growing_patterns)
        shift = min(new_plants) - min(plants)
        if shift_plants(plants, shift) == new_plants:
            remaining = generations - (generation + 1)
            return shift_plants(new_plants, shift * remaining)
        plants = new_plants
    return plants


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    # "initial state: #..#.#..##......###...###"
    initial_state = lines[0].split(": ")[1]
    plants = set()
    for pot, symbol in enumerate(initial_state):
        if symbol == "#":
            plants.add(pot)
    # "...## => #"; only the patterns that produce a plant matter.
    growing_patterns = set()
    for line in lines[2:]:
        pattern, result = line.split(" => ")
        if result == "#":
            growing_patterns.add(pattern)

    ##########
    # part 1 #
    ##########
    part_1 = sum(simulate(plants, growing_patterns, GENERATIONS))
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = sum(simulate(plants, growing_patterns, MANY_GENERATIONS))
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
