import os


def compare(a, b):
    count = 0
    for v1, v2 in zip(a, b):
        count += sum(1 for c1, c2 in zip(v1, v2) if c1 != c2)
    return count


def transpose(pattern):
    return ["".join(line[c] for line in pattern) for c in range(len(pattern[0]))]


def reflection(pattern, smudges):
    for r in range(1, len(pattern)):
        before = pattern[:r]
        after = pattern[r:]
        size = min(len(before), len(after))
        if compare(before[::-1][:size], after[:size]) == smudges:
            return r
    return None


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    patterns = [p.split("\n") for p in file.read().strip().split("\n\n")]

    ##########
    # part 1 #
    ##########
    part_1 = 0
    for p in patterns:
        horiz_reflect = reflection(p, 0)
        if horiz_reflect:
            part_1 += horiz_reflect * 100
        else:
            part_1 += reflection(transpose(p), 0)
    print(part_1)

    ##########
    # part 2 #
    ##########
    part_2 = 0
    for p in patterns:
        horiz_reflect = reflection(p, 1)
        if horiz_reflect:
            part_2 += horiz_reflect * 100
        else:
            part_2 += reflection(transpose(p), 1)
    print(part_2)


if __name__ == "__main__":
    main()
