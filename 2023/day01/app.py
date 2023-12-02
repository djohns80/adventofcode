import os
import re


def replace_number_words(line):
    numbers = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    i = 0
    while i < len(line):
        for k, v in numbers.items():
            if line[i:].startswith(k):
                line = f"{line[0:i]}{v}{line[len(k)+i:]}"
        i += 1
    return line


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
    lines = [line.strip() for line in content.splitlines()]

    part_1 = 0
    for line in lines:
        digits = "".join(re.findall(r"[0-9]", line))
        part_1 += int(f"{digits[0]}{digits[-1]}")
    print(part_1)

    ##########
    # part 2 #
    ##########
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = [line.strip() for line in content.splitlines()]

    numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    part_2 = 0
    for line in lines:
        digits = [None for i in range(len(line))]
        for m1 in re.finditer(r"\d", line):
            digits[m1.start()] = int(m1.group())
        for k, v in numbers.items():
            for m2 in re.finditer(k, line):
                digits[m2.start()] = v
        digits = [d for d in digits if d]
        part_2 += int(f"{digits[0]}{digits[-1]}")
    print(part_2)


if __name__ == "__main__":
    main()
