import os
import re

CODE_1 = 20151125
MULTIPLY = 252533
DIVIDE = 33554393


def pos_number(row, col):
    diagonal = row + col - 1
    codes_before = (diagonal - 1) * diagonal // 2
    return codes_before + col


def number_code(number):
    return (pow(MULTIPLY, number - 1, DIVIDE) * CODE_1) % DIVIDE


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    row, col = map(int, re.findall(r"\d+", content))

    ##########
    # part 1 #
    ##########
    print("part 1:", number_code(pos_number(row, col)))


if __name__ == "__main__":
    main()
