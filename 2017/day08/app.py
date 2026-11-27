import operator
import os

COMPARISONS = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}
DIRECTIONS = {"inc": 1, "dec": -1}


def parse_instructions(lines):
    """Return a list of (register, change, condition register, comparison, value)."""
    instructions = []
    for line in lines:
        if not line.strip():
            continue
        register, direction, amount, _, condition_register, comparison, value = (
            line.split()
        )
        change = DIRECTIONS[direction] * int(amount)
        instructions.append(
            (register, change, condition_register, comparison, int(value))
        )
    return instructions


def run_instructions(instructions):
    """Process every instruction.

    Returns the final register values and the highest value any register held
    along the way.
    """
    registers = {}
    highest_value = 0  # every register starts at 0
    for register, change, condition_register, comparison, value in instructions:
        condition_value = registers.get(condition_register, 0)
        if COMPARISONS[comparison](condition_value, value):
            registers[register] = registers.get(register, 0) + change
            highest_value = max(highest_value, registers[register])
    return registers, highest_value


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    instructions = parse_instructions(lines)
    registers, highest_value = run_instructions(instructions)

    ##########
    # part 1 #
    ##########
    part_1 = max(registers.values())
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = highest_value
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
