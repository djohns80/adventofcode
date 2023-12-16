import os

directions = {
    "down": (1, 0),
    "up": (-1, 0),
    "right": (0, 1),
    "left": (0, -1),
}


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))
    rows = len(lines)
    cols = len(lines[0])
    grid = {(y, x): t for y, line in enumerate(lines) for x, t in enumerate(list(line))}
    energized = {}

    def move(tile, direction):
        next_moves = []
        if grid[tile] == ".":
            next_moves = [
                (
                    (
                        tile[0] + directions[direction][0],
                        tile[1] + directions[direction][1],
                    ),
                    direction,
                )
            ]
        elif grid[tile] == "/":
            match direction:
                case "left":
                    direction = "down"
                case "right":
                    direction = "up"
                case "up":
                    direction = "right"
                case "down":
                    direction = "left"
            next_moves = [
                (
                    (
                        tile[0] + directions[direction][0],
                        tile[1] + directions[direction][1],
                    ),
                    direction,
                )
            ]
        elif grid[tile] == "\\":
            match direction:
                case "left":
                    direction = "up"
                case "right":
                    direction = "down"
                case "up":
                    direction = "left"
                case "down":
                    direction = "right"
            next_moves = [
                (
                    (
                        tile[0] + directions[direction][0],
                        tile[1] + directions[direction][1],
                    ),
                    direction,
                )
            ]
        elif grid[tile] == "|":
            match direction:
                case "left" | "right":
                    next_moves = [
                        ((tile[0] + directions[d][0], tile[1] + directions[d][1]), d)
                        for d in ["up", "down"]
                    ]
                case _:
                    next_moves = [
                        (
                            (
                                tile[0] + directions[direction][0],
                                tile[1] + directions[direction][1],
                            ),
                            direction,
                        )
                    ]
        elif grid[tile] == "-":
            match direction:
                case "up" | "down":
                    next_moves = [
                        ((tile[0] + directions[d][0], tile[1] + directions[d][1]), d)
                        for d in ["left", "right"]
                    ]
                case _:
                    next_moves = [
                        (
                            (
                                tile[0] + directions[direction][0],
                                tile[1] + directions[direction][1],
                            ),
                            direction,
                        )
                    ]
        valid_moves = []
        for m in next_moves:
            if 0 <= m[0][0] < rows and 0 <= m[0][1] < cols:
                if m not in energized:
                    energized.add(m)
                    valid_moves.append(m)
        return valid_moves

    starting_moves = []
    for r in range(rows):
        starting_moves.extend([((r, 0), "right"), ((r, cols - 1), "left")])
    for c in range(cols):
        starting_moves.extend([((0, c), "down"), ((rows - 1, c), "up")])

    results = {}
    for start in starting_moves:
        energized = {start}
        moves = [start]
        while len(moves) > 0:
            moves = [v for m in moves for v in move(*m)]
        results[start] = len(set([m[0] for m in energized]))

    ##########
    # part 1 #
    ##########
    # energized = {((0, 0), "right")}
    # moves = [((0, 0), "right")]
    # while len(moves) > 0:
    #     moves = [v for m in moves for v in move(*m)]
    # print(len(set([m[0] for m in energized])))
    print(results[((0, 0), "right")])

    ##########
    # part 2 #
    ##########
    print(max(results.values()))


if __name__ == "__main__":
    main()
