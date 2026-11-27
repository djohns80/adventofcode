import os

INITIAL_SCORES = (3, 7)
SCORES_WANTED = 10
# part 2: recipes to make between each search of the scoreboard
SEARCH_CHUNK = 1_000_000


def create_recipes(scoreboard, elves, target_length):
    """
    Keep combining the two elves' current recipes until the scoreboard has at
    least target_length recipes. Each round appends the digits of the sum,
    then each elf steps forward 1 + its current score.
    Mutates the scoreboard and returns the elves' new positions.
    """
    # part 2 needs ~20 million recipes, so the loop below is kept tight: two plain
    # int positions, a bytearray scoreboard and the digits of every possible
    # sum of two scores (0 to 18) worked out up front
    new_recipes = []
    for total in range(19):
        new_recipes.append(bytes(int(digit) for digit in str(total)))

    elf_1, elf_2 = elves
    while len(scoreboard) < target_length:
        score_1 = scoreboard[elf_1]
        score_2 = scoreboard[elf_2]
        scoreboard += new_recipes[score_1 + score_2]
        size = len(scoreboard)
        elf_1 = (elf_1 + 1 + score_1) % size
        elf_2 = (elf_2 + 1 + score_2) % size
    return elf_1, elf_2


def scores_after(recipe_count, scores_wanted):
    """The scores of the recipes immediately after the first recipe_count, as a string."""
    scoreboard = bytearray(INITIAL_SCORES)
    create_recipes(scoreboard, (0, 1), recipe_count + scores_wanted)
    result = ""
    for score in scoreboard[recipe_count : recipe_count + scores_wanted]:
        result += str(score)
    return result


def recipes_before(digits):
    """How many recipes are to the left of the first appearance of the score sequence."""
    sequence = bytes(int(digit) for digit in digits)
    scoreboard = bytearray(INITIAL_SCORES)
    elves = (0, 1)
    search_from = 0
    while True:
        elves = create_recipes(scoreboard, elves, len(scoreboard) + SEARCH_CHUNK)
        position = scoreboard.find(sequence, search_from)
        if position != -1:
            return position
        # the sequence may straddle the end of this chunk, so overlap the next search
        search_from = max(0, len(scoreboard) - len(sequence) + 1)


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    # keep the digits as text too: leading zeros matter in part 2
    puzzle_input = content.strip()

    ##########
    # part 1 #
    ##########
    part_1 = scores_after(int(puzzle_input), SCORES_WANTED)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = recipes_before(puzzle_input)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
