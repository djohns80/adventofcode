import os

LIST_SIZE = 256
HASH_SUFFIX = [17, 31, 73, 47, 23]
HASH_ROUNDS = 64
BLOCK_SIZE = 16


def reverse_span(marks, start, length):
    """Reverse length marks starting at start, wrapping around the circular list."""
    size = len(marks)
    for offset in range(length // 2):
        left = (start + offset) % size
        right = (start + length - 1 - offset) % size
        marks[left], marks[right] = marks[right], marks[left]


def tie_knots(marks, lengths, position=0, skip_size=0):
    """Tie one knot per length, changing marks in place.

    Returns the final position and skip size so further rounds can continue.
    """
    for length in lengths:
        reverse_span(marks, position, length)
        position = (position + length + skip_size) % len(marks)
        skip_size += 1
    return position, skip_size


def knot_hash(text):
    """Return the full knot hash of text as 32 hexadecimal digits."""
    lengths = []
    for character in text:
        lengths.append(ord(character))
    lengths.extend(HASH_SUFFIX)

    marks = list(range(LIST_SIZE))
    position = 0
    skip_size = 0
    for _ in range(HASH_ROUNDS):
        position, skip_size = tie_knots(marks, lengths, position, skip_size)

    # dense hash: XOR together each block of 16 marks
    hex_digits = ""
    for block_start in range(0, LIST_SIZE, BLOCK_SIZE):
        block_value = 0
        for mark in marks[block_start : block_start + BLOCK_SIZE]:
            block_value ^= mark
        hex_digits += f"{block_value:02x}"
    return hex_digits


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    text = content.strip()

    ##########
    # part 1 #
    ##########
    lengths = []
    for value in text.split(","):
        lengths.append(int(value))
    marks = list(range(LIST_SIZE))
    tie_knots(marks, lengths)
    part_1 = marks[0] * marks[1]
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = knot_hash(text)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
