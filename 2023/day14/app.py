import os


def tilt(values):
    moves = True
    while moves:
        moves = False
        for i in range(len(values) - 1):
            if values[i] == "." and values[i + 1] == "O":
                values[i] = "O"
                values[i + 1] = "."
                moves = True
    return values


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))
    rows = len(lines)
    cols = len(lines[0])
    grid = {(y, x): c for y, line in enumerate(lines) for x, c in enumerate(list(line))}

    # def print_grid(data):
    #     for y in range(rows):
    #         print("".join(data[(y, x)] for x in range(cols)))

    def tilt_north(data):
        for c in range(cols):
            col = [v for d, v in data.items() if d[1] == c]
            for r, v in enumerate(tilt(col)):
                data[(r, c)] = v

    def tilt_west(data):
        for r in range(rows):
            col = [v for d, v in data.items() if d[0] == r]
            for c, v in enumerate(tilt(col)):
                data[(r, c)] = v

    def tilt_south(data):
        for c in range(cols):
            col = [v for d, v in data.items() if d[1] == c]
            for r, v in enumerate(reversed(tilt(list(reversed(col))))):
                data[(r, c)] = v

    def tilt_east(data):
        for r in range(rows):
            col = [v for d, v in data.items() if d[0] == r]
            for c, v in enumerate(reversed(tilt(list(reversed(col))))):
                data[(r, c)] = v

    def cycle(data):
        tilt_north(data)
        tilt_west(data)
        tilt_south(data)
        tilt_east(data)
        return sum(rows - k[0] for k, v in data.items() if v == "O")

    ##########
    # part 1 #
    ##########
    # data_1 = grid.copy()
    # tilt_north(data_1)
    # print(sum(rows - k[0] for k, v in data_1.items() if v == "O"))

    ##########
    # part 2 #
    ##########
    data_2 = grid.copy()
    results = []
    cycles = 150  # arbitrary number of cycles to find the cycle increase as needed
    pattern_match_length = 5
    for _ in range(cycles):
        results.append(cycle(data_2))
    loops = [
        i
        for i in range(len(results) - (pattern_match_length - 1))
        if results[i : i + pattern_match_length] == results[-pattern_match_length:]
    ]
    loop_length = loops[-1] - loops[-2]
    result_loop = results[len(results) - loop_length - 1 :][:-1]
    remainder = cycles % loop_length
    print(result_loop[(1000000000 - remainder) % loop_length])


if __name__ == "__main__":
    main()
