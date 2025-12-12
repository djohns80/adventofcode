import os


def rotate_90(positions):
    return [(-y, x) for x, y in positions]


def flip_horizontal(positions):
    return [(-x, y) for x, y in positions]


def shift_to_origin(positions):
    if not positions:
        return positions
    min_x = min(x for x, _ in positions)
    min_y = min(y for _, y in positions)
    return [(x - min_x, y - min_y) for x, y in positions]


def get_all_orientations(positions):
    orientations = set()
    current = positions
    for _ in range(4):
        orientations.add(tuple(sorted(shift_to_origin(current))))
        current = rotate_90(current)
    current = flip_horizontal(positions)
    for _ in range(4):
        orientations.add(tuple(sorted(shift_to_origin(current))))
        current = rotate_90(current)
    return [list(orient) for orient in orientations]


def can_place(grid, shape, x, y, width, height):
    for dx, dy in shape:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= width or ny < 0 or ny >= height or grid[ny][nx]:
            return False
    return True


def place(grid, shape, x, y):
    for dx, dy in shape:
        grid[y + dy][x + dx] = True


def remove(grid, shape, x, y):
    for dx, dy in shape:
        grid[y + dy][x + dx] = False


def solve_region(shapes, width, height, counts):
    # Build list of all presents we need to place, calculating total area to exlcude regions that are not big enough
    pieces = []
    total_area = 0
    for shape_id, count in enumerate(counts):
        if count > 0 and shape_id in shapes:
            area = len(shapes[shape_id])
            total_area += area * count
            pieces.extend([shape_id] * count)
    if total_area > width * height:
        return False
    if not pieces:
        return True

    # Generate list of all possible orientations of each shape
    orientations = {}
    for shape_id in set(pieces):
        orientations[shape_id] = get_all_orientations(shapes[shape_id])

    # Prepare empty region grid
    grid = [[False] * width for _ in range(height)]

    def place_presents(index):
        # Check if we have completed all pieces
        if index == len(pieces):
            return True
        shape_id = pieces[index]
        # Test every possible orientation
        for orientation in orientations[shape_id]:
            for y in range(height):
                for x in range(width):
                    if can_place(grid, orientation, x, y, width, height):
                        place(grid, orientation, x, y)
                        if place_presents(index + 1):
                            return True
                        remove(grid, orientation, x, y)
        return False

    return place_presents(0)


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    sections = content.strip().split("\n\n")
    shapes = {}
    for section in sections[:-1]:
        lines = section.split("\n")
        shape_id = int(lines[0].split(":")[0])
        positions = []
        for y, line in enumerate(lines[1:]):
            for x, char in enumerate(line):
                if char == "#":
                    positions.append((x, y))
        shapes[shape_id] = positions
    regions = []
    for line in sections[-1].split("\n"):
        parts = line.split(":")
        width, height = map(int, parts[0].split("x"))
        counts = list(map(int, parts[1].split()))
        regions.append((width, height, counts))

    ##########
    # part 1 #
    ##########
    part_1 = 0
    for width, height, counts in regions:
        if solve_region(shapes, width, height, counts):
            part_1 += 1
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # print("part 2:", part_2)


if __name__ == "__main__":
    main()
