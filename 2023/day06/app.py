import os
import math
import re


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))

    ##########
    # part 1 #
    ##########
    data = list(
        zip(
            *[
                list(map(int, line.strip().split(":")[1].strip().split()))
                for line in lines
            ]
        )
    )
    print(
        math.prod(
            [len([t for h in range(t + 1) if ((t - h) * h) > r_d]) for t, r_d in data]
        )
    )

    ##########
    # part 2 #
    ##########
    data = list(map(int, ["".join(re.findall(r"\d+", line)) for line in lines]))
    count = 0
    for h in range(data[0] + 1):
        if ((data[0] - h) * h) > data[1]:
            count += 1
    print(count)


if __name__ == "__main__":
    main()
