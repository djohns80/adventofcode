import os
import re
import math


def main():
    ##########
    # part 1 #
    ##########
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    memory = content.strip()
    instructions1 = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", memory)
    print(sum(math.prod(map(int, i)) for i in instructions1))

    ##########
    # part 2 #
    ##########
    instructions2 = re.findall(
        r"(?:mul\(\d{1,3},\d{1,3}\))|(?:do\(\))|(?:don\'t\(\))", memory
    )
    enabled = True
    part_2 = 0
    for i in instructions2:
        if i == "do()":
            enabled = True
        elif i == "don't()":
            enabled = False
        else:
            if enabled:
                part_2 += math.prod(map(int, re.findall(r"\d{1,3}", i)))
    print(part_2)


if __name__ == "__main__":
    main()
