import os
import re
import math
from collections import deque


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    equations = [
        list(map(int, re.findall(r"\d+", line))) for line in content.splitlines()
    ]

    calculations = deque((eq, [], eq[1], 0) for eq in equations)
    true_equations_1 = []
    true_equations_2 = []
    while calculations:
        equ, ops, cur, pos = calculations.pop()
        if pos <= len(equ[1:]) - 2:
            test1 = sum((cur, equ[pos + 2]))
            if test1 <= equ[0]:
                calculations.append((equ, [*ops, "+"], test1, pos + 1))
            test2 = math.prod((cur, equ[pos + 2]))
            if test2 <= equ[0]:
                calculations.append((equ, [*ops, "*"], test2, pos + 1))
            test3 = int(f"{cur}{equ[pos + 2]}")
            if test3 <= equ[0]:
                calculations.append((equ, [*ops, "||"], test3, pos + 1))
        else:
            if cur == equ[0]:
                true_equations_2.append(tuple(equ))
                if "||" not in ops:
                    true_equations_1.append(tuple(equ))

    ##########
    # part 1 #
    ##########
    print(sum(t[0] for t in set(true_equations_1)))

    ##########
    # part 2 #
    ##########
    print(sum(t[0] for t in set(true_equations_2)))


if __name__ == "__main__":
    main()
