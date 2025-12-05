import os


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    fresh_raw, available_raw = content.split("\n\n")
    fresh_int = [
        tuple(int(v) for v in line.strip().split("-"))
        for line in fresh_raw.splitlines()
    ]
    fresh_sorted = sorted(fresh_int, key=lambda tup: tup[0])
    fresh_merged = []
    for start, end in fresh_sorted:
        if fresh_merged and start <= fresh_merged[-1][1] + 1:
            fresh_merged[-1] = (fresh_merged[-1][0], max(fresh_merged[-1][1], end))
        else:
            fresh_merged.append((start, end))
    fresh = [range(start, end + 1) for start, end in fresh_merged]
    available = [int(line.strip()) for line in available_raw.splitlines()]

    ##########
    # part 1 #
    ##########
    part_1 = 0
    for a in available:
        for f in fresh:
            if a in f:
                part_1 += 1
                break
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = sum(len(f) for f in fresh)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
