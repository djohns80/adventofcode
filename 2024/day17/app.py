import os
import re
from collections import deque


def run_program(program, register):
    pointer = 0

    def combo(operand):
        return (
            (register["A"], register["B"], register["C"])[operand - 4]
            if operand >= 4
            else operand
        )

    output = []
    while pointer < len(program) - 1:
        opcode, operand = program[pointer], program[pointer + 1]
        match opcode:
            case 0:
                register["A"] //= 2 ** combo(operand)
            case 1:
                register["B"] ^= operand
            case 2:
                register["B"] = combo(operand) & 7
            case 3:
                if register["A"]:
                    pointer = operand - 2
            case 4:
                register["B"] ^= register["C"]
            case 5:
                output.append(combo(operand) & 7)
            case 6:
                register["B"] = register["A"] // 2 ** combo(operand)
            case 7:
                register["C"] = register["A"] // 2 ** combo(operand)
        pointer += 2
    return output


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    a, b, c, *program = map(int, re.findall(r"\d+", file.read()))

    ##########
    # part 1 #
    ##########
    print(",".join(list(map(str, run_program(program, {"A": a, "B": b, "C": c})))))

    ##########
    # part 2 #
    ##########
    candidates = deque([0])
    min_candidate = 2 ** (3 * (len(program) - 1))
    while candidates and candidates[-1] < min_candidate:
        seed = candidates.popleft()
        for a in range(2**6):
            a += seed << 6
            output = run_program(program, {"A": a, "B": 0, "C": 0})
            if a < 8:
                output.insert(0, 0)
            if output == program[-(len(output)) :]:
                candidates.append(a)
            if output == program:
                break
    print(candidates[-1])


if __name__ == "__main__":
    main()
