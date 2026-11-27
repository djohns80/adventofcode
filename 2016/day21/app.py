import itertools
import os

PASSWORD = "abcdefgh"
SCRAMBLED_PASSWORD = "fbgdceah"


def rotate_right(letters, steps):
    steps %= len(letters)
    if steps == 0:
        return letters
    return letters[-steps:] + letters[:-steps]


def rotate_left(letters, steps):
    steps %= len(letters)
    return letters[steps:] + letters[:steps]


def apply_operation(letters, words):
    """Apply one scrambling operation (given as a list of words) to a list of letters."""
    match words:
        case ["swap", "position", x, "with", "position", y]:
            x, y = int(x), int(y)
            letters[x], letters[y] = letters[y], letters[x]
        case ["swap", "letter", x, "with", "letter", y]:
            x, y = letters.index(x), letters.index(y)
            letters[x], letters[y] = letters[y], letters[x]
        case ["rotate", "left", steps, _]:
            letters = rotate_left(letters, int(steps))
        case ["rotate", "right", steps, _]:
            letters = rotate_right(letters, int(steps))
        case ["rotate", "based", "on", "position", "of", "letter", letter]:
            index = letters.index(letter)
            steps = 1 + index
            if index >= 4:
                steps += 1
            letters = rotate_right(letters, steps)
        case ["reverse", "positions", x, "through", y]:
            x, y = int(x), int(y)
            letters = letters[:x] + letters[x : y + 1][::-1] + letters[y + 1 :]
        case ["move", "position", x, "to", "position", y]:
            letter = letters.pop(int(x))
            letters.insert(int(y), letter)
        case _:
            raise ValueError(f"unknown operation: {' '.join(words)}")
    return letters


def scramble(password, operations):
    letters = list(password)
    for words in operations:
        letters = apply_operation(letters, words)
    return "".join(letters)


def unscramble(scrambled, operations):
    """Find the password that scrambles to the given result.

    Rather than inverting each operation, try every ordering of the letters
    (8! = 40,320 for 8 letters) through the same scramble function.
    """
    for candidate in itertools.permutations(scrambled):
        if scramble(candidate, operations) == scrambled:
            return "".join(candidate)
    return None


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    operations = []
    for line in lines:
        operations.append(line.split())

    ##########
    # part 1 #
    ##########
    part_1 = scramble(PASSWORD, operations)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = unscramble(SCRAMBLED_PASSWORD, operations)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
