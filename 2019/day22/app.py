import os

DECK_SIZE = 10007
CARD_TO_TRACK = 2019

BIG_DECK_SIZE = 119315717514047
SHUFFLE_REPEATS = 101741582076661
TARGET_POSITION = 2020

# Every technique moves a card from position p to (a * p + b) % deck_size:
#   deal into new stack:     p -> -p - 1     (a = -1, b = -1)
#   cut N:                   p -> p - N      (a = 1,  b = -N)
#   deal with increment N:   p -> p * N      (a = N,  b = 0)
# Doing one such map after another is again a map of the same shape, so the whole
# shuffle, and even the shuffle repeated a huge number of times, is just one (a, b).
# Going backwards (which card ends up at a position) solves a * card + b = position,
# which works because the deck sizes are prime, so a always has a modular inverse.


def parse_technique(line):
    """Turn a line into (name, amount); "deal into new stack" has no amount."""
    if line == "deal into new stack":
        return ("new stack", 0)
    if line.startswith("cut "):
        return ("cut", int(line.split()[-1]))
    if line.startswith("deal with increment "):
        return ("increment", int(line.split()[-1]))
    raise ValueError(f"unknown technique: {line}")


def technique_as_map(technique, deck_size):
    """The (a, b) of the map p -> a * p + b that one technique applies to a position."""
    name, amount = technique
    if name == "new stack":
        # the deck is reversed
        return (-1 % deck_size, -1 % deck_size)
    if name == "cut":
        # everything moves up by amount, wrapping around (also works for negative cuts)
        return (1, -amount % deck_size)
    if name == "increment":
        # the card dealt at step i lands at i * amount
        return (amount % deck_size, 0)
    raise ValueError(f"unknown technique: {name}")


def combine_maps(first, second, deck_size):
    """The single map that does first and then second."""
    first_a, first_b = first
    second_a, second_b = second
    # second_a * (first_a * p + first_b) + second_b
    return (
        (second_a * first_a) % deck_size,
        (second_a * first_b + second_b) % deck_size,
    )


def repeat_map(linear_map, times, deck_size):
    """Apply a map many times, by repeated squaring like modular exponentiation."""
    result = (1, 0)  # p -> p, doing nothing
    power = linear_map  # the map applied 1, 2, 4, 8, ... times
    while times > 0:
        if times % 2 == 1:
            result = combine_maps(result, power, deck_size)
        power = combine_maps(power, power, deck_size)
        times //= 2
    return result


def shuffle_position(techniques, position, deck_size, repeats=1, backwards=False):
    """
    Where the card starting at this position ends up after shuffling repeats times.
    With backwards=True, the starting position of the card that ends up at position.
    """
    shuffle_map = (1, 0)
    for technique in techniques:
        technique_map = technique_as_map(technique, deck_size)
        shuffle_map = combine_maps(shuffle_map, technique_map, deck_size)
    a, b = repeat_map(shuffle_map, repeats, deck_size)
    if backwards:
        return ((position - b) * pow(a, -1, deck_size)) % deck_size
    return (a * position + b) % deck_size


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    techniques = []
    for line in lines:
        if line:
            techniques.append(parse_technique(line))

    ##########
    # part 1 #
    ##########
    # cards start at the position matching their number
    part_1 = shuffle_position(techniques, CARD_TO_TRACK, DECK_SIZE)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # the card's starting position is also its number
    part_2 = shuffle_position(
        techniques,
        TARGET_POSITION,
        BIG_DECK_SIZE,
        repeats=SHUFFLE_REPEATS,
        backwards=True,
    )
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
