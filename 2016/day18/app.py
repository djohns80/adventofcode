import os

TOTAL_ROWS = 40
TOTAL_ROWS_PART_2 = 400000
TRAP = "^"


def row_to_bits(row):
    # each tile becomes one bit (trap = 1, safe = 0), leftmost tile highest
    bits = 0
    for tile in row:
        bits = bits * 2
        if tile == TRAP:
            bits += 1
    return bits


def count_safe_tiles(first_row, total_rows):
    width = len(first_row)
    all_tiles = (1 << width) - 1
    row = row_to_bits(first_row)
    safe_count = 0
    for _ in range(total_rows):
        safe_count += width - row.bit_count()
        # All four trap rules boil down to "left and right tiles differ",
        # so the next row is (left neighbours) XOR (right neighbours).
        # Shifting moves every tile's neighbour into its place; the walls
        # shift in as 0 (safe), and the mask drops the bit pushed off the end.
        row = ((row << 1) ^ (row >> 1)) & all_tiles
    return safe_count


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    first_row = content.strip()

    ##########
    # part 1 #
    ##########
    part_1 = count_safe_tiles(first_row, TOTAL_ROWS)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = count_safe_tiles(first_row, TOTAL_ROWS_PART_2)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
