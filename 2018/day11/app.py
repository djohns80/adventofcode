import os

GRID_SIZE = 300
SQUARE_SIZE = 3


def power_level(x, y, serial_number):
    rack_id = x + 10
    power = rack_id * y
    power += serial_number
    power *= rack_id
    hundreds_digit = (power // 100) % 10
    return hundreds_digit - 5


def build_summed_area_table(serial_number, grid_size):
    """Return a table where table[y][x] is the total power of every cell from
    (1, 1) to (x, y) inclusive. Row and column 0 are all zero, which avoids
    special cases at the edges."""
    table = []
    for _ in range(grid_size + 1):
        table.append([0] * (grid_size + 1))
    for y in range(1, grid_size + 1):
        for x in range(1, grid_size + 1):
            table[y][x] = (
                power_level(x, y, serial_number)
                + table[y - 1][x]
                + table[y][x - 1]
                - table[y - 1][x - 1]
            )
    return table


def square_power(table, x, y, size):
    """Return the total power of the size x size square with top-left cell (x, y)."""
    right = x + size - 1
    bottom = y + size - 1
    return (
        table[bottom][right]
        - table[y - 1][right]
        - table[bottom][x - 1]
        + table[y - 1][x - 1]
    )


def best_square(table, grid_size, smallest_size, largest_size):
    """Return (x, y, size, total) for the square with the largest total power,
    trying every square size from smallest_size to largest_size inclusive."""
    best = None
    best_total = None
    for size in range(smallest_size, largest_size + 1):
        for y in range(1, grid_size - size + 2):
            for x in range(1, grid_size - size + 2):
                total = square_power(table, x, y, size)
                if best_total is None or total > best_total:
                    best_total = total
                    best = (x, y, size, total)
    return best


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    serial_number = int(content.strip())
    table = build_summed_area_table(serial_number, GRID_SIZE)

    ##########
    # part 1 #
    ##########
    x, y, _, _ = best_square(table, GRID_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    part_1 = f"{x},{y}"
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    x, y, size, _ = best_square(table, GRID_SIZE, 1, GRID_SIZE)
    part_2 = f"{x},{y},{size}"
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
