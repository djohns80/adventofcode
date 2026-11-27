import os

GRID_SIZE = 128
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


def build_grid(key):
    """Return the disk as a list of rows, each a list of booleans (True = used)."""
    grid = []
    for row_number in range(GRID_SIZE):
        row = []
        for hex_digit in knot_hash(f"{key}-{row_number}"):
            for bit in f"{int(hex_digit, 16):04b}":
                row.append(bit == "1")
        grid.append(row)
    return grid


def count_used(grid):
    used = 0
    for row in grid:
        for square in row:
            if square:
                used += 1
    return used


def count_regions(grid):
    """Return how many groups of orthogonally adjacent used squares there are."""
    seen = set()
    region_count = 0
    for start_row in range(len(grid)):
        for start_column in range(len(grid[start_row])):
            if not grid[start_row][start_column] or (start_row, start_column) in seen:
                continue
            # a new region: flood fill every used square connected to it
            region_count += 1
            seen.add((start_row, start_column))
            to_visit = [(start_row, start_column)]
            while to_visit:
                row, column = to_visit.pop()
                for next_row, next_column in (
                    (row - 1, column),
                    (row + 1, column),
                    (row, column - 1),
                    (row, column + 1),
                ):
                    if (
                        0 <= next_row < len(grid)
                        and 0 <= next_column < len(grid[next_row])
                        and grid[next_row][next_column]
                        and (next_row, next_column) not in seen
                    ):
                        seen.add((next_row, next_column))
                        to_visit.append((next_row, next_column))
    return region_count


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    key = content.strip()
    grid = build_grid(key)

    ##########
    # part 1 #
    ##########
    part_1 = count_used(grid)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = count_regions(grid)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
