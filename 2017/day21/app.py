import os

START_PATTERN = ".#./..#/###"
ITERATIONS = 5
MORE_ITERATIONS = 18


def pattern_to_grid(pattern):
    return tuple(pattern.split("/"))


def rotate(grid):
    # rotate 90 degrees clockwise: the new row i is the old column i read bottom-up
    size = len(grid)
    rotated = []
    for column in range(size):
        new_row = ""
        for row in range(size - 1, -1, -1):
            new_row += grid[row][column]
        rotated.append(new_row)
    return tuple(rotated)


def flip(grid):
    # mirror left-to-right
    flipped = []
    for row in grid:
        flipped.append(row[::-1])
    return tuple(flipped)


def all_orientations(grid):
    # the 4 rotations of the grid plus the 4 rotations of its mirror image
    orientations = []
    for start in (grid, flip(grid)):
        current = start
        for _ in range(4):
            orientations.append(current)
            current = rotate(current)
    return orientations


def parse_rules(lines):
    # store every rotated/flipped version of each input pattern so that
    # matching a square later is a simple dictionary lookup
    rules = {}
    for line in lines:
        input_pattern, output_pattern = line.split(" => ")
        output_grid = pattern_to_grid(output_pattern)
        for orientation in all_orientations(pattern_to_grid(input_pattern)):
            rules[orientation] = output_grid
    return rules


def enhance(grid, rules):
    size = len(grid)
    if size % 2 == 0:
        block_size = 2
    else:
        block_size = 3
    blocks_per_side = size // block_size
    new_block_size = block_size + 1

    new_grid = []
    for block_row in range(blocks_per_side):
        # each row of blocks becomes new_block_size rows of the new grid
        new_rows = [""] * new_block_size
        top = block_row * block_size
        for block_column in range(blocks_per_side):
            left = block_column * block_size
            block = []
            for row in grid[top : top + block_size]:
                block.append(row[left : left + block_size])
            output_block = rules[tuple(block)]
            for row in range(new_block_size):
                new_rows[row] += output_block[row]
        new_grid.extend(new_rows)
    return tuple(new_grid)


def count_on_after(rules, iterations):
    grid = pattern_to_grid(START_PATTERN)
    for _ in range(iterations):
        grid = enhance(grid, rules)
    on_count = 0
    for row in grid:
        on_count += row.count("#")
    return on_count


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    rules = parse_rules(lines)

    ##########
    # part 1 #
    ##########
    part_1 = count_on_after(rules, ITERATIONS)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = count_on_after(rules, MORE_ITERATIONS)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
