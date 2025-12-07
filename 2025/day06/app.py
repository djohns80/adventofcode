import os
import math


def calculate_result(operands, operator):
    match operator:
        case "*":
            return math.prod(operands)
        case "+":
            return sum(operands)


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()

    ##########
    # part 1 #
    ##########
    values = [[int(v) for v in line.split()] for line in lines[:-1]]
    operands = list(zip(*values))
    operators = lines[-1].split()
    part_1 = sum(calculate_result(operands[i], op) for i, op in enumerate(operators))
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # Rotate the input
    rotated = [
        "".join(lines[row][col] for row in range(len(lines)))
        for col in range(len(lines[0]) - 1, -1, -1)
    ]
    # Parse problems
    problems = []
    current = []
    for line in rotated:
        line = line.strip()
        if not line:
            if current:
                problems.append(current)
                current = []
        else:
            current.append(line)
    if current:
        problems.append(current)
    part_2 = sum(
        calculate_result(
            [int(problem[-1][:-1])] + [int(line) for line in problem[:-1]],
            problem[-1][-1],
        )
        for problem in problems
        if problem
    )
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
