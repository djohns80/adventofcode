import os

STARTING_A_PART_1 = 7  # the number of eggs
STARTING_A_PART_2 = 12  # the real number of eggs


def get_value(argument, registers):
    """An argument is either a register name or an integer."""
    if argument in registers:
        return registers[argument]
    return int(argument)


def toggle(instruction):
    """Toggle an instruction in place (its arguments are left unchanged)."""
    if len(instruction) == 2:
        instruction[0] = "dec" if instruction[0] == "inc" else "inc"
    else:
        instruction[0] = "cpy" if instruction[0] == "jnz" else "jnz"


def try_multiply(program, pointer, registers):
    """Speed-up for this nested loop, which adds source * outer to target one at a time:

        cpy source inner
        inc target
        dec inner
        jnz inner -2
        dec outer
        jnz outer -5

    If the six instructions at the pointer form that loop *right now*, do the
    multiplication in one go and return True. Because the check uses the current
    program, an instruction changed by tgl just stops the pattern from matching
    and the loop is run normally instead.
    """
    match program[pointer : pointer + 6]:
        case [
            ["cpy", source, inner],
            ["inc", target],
            ["dec", inner_2],
            ["jnz", inner_3, "-2"],
            ["dec", outer],
            ["jnz", outer_2, "-5"],
        ] if inner == inner_2 == inner_3 and outer == outer_2:
            pass
        case _:
            return False
    # the shortcut is only the same as running the loop when it uses three
    # different registers and both counters start positive
    loop_registers = {target, inner, outer}
    if len(loop_registers) < 3 or not loop_registers.issubset(registers):
        return False
    if source in loop_registers:
        return False
    multiplier = get_value(source, registers)
    if multiplier <= 0 or registers[outer] <= 0:
        return False
    registers[target] += multiplier * registers[outer]
    registers[inner] = 0
    registers[outer] = 0
    return True


def run(program, registers):
    """Run the assembunny program and return the final registers."""
    # copy everything, because tgl modifies the program while it runs
    program = [list(instruction) for instruction in program]
    registers = dict(registers)
    pointer = 0
    while 0 <= pointer < len(program):
        if try_multiply(program, pointer, registers):
            pointer += 6
            continue
        match program[pointer]:
            case ["cpy", source, target]:
                # a toggled instruction like "cpy 1 2" is invalid, so skip it
                if target in registers:
                    registers[target] = get_value(source, registers)
            case ["inc", target]:
                if target in registers:
                    registers[target] += 1
            case ["dec", target]:
                if target in registers:
                    registers[target] -= 1
            case ["jnz", condition, offset]:
                if get_value(condition, registers) != 0:
                    pointer += get_value(offset, registers)
                    continue
            case ["tgl", offset]:
                target_pointer = pointer + get_value(offset, registers)
                if 0 <= target_pointer < len(program):
                    toggle(program[target_pointer])
        pointer += 1
    return registers


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    program = []
    for line in lines:
        program.append(line.split())

    ##########
    # part 1 #
    ##########
    registers = {"a": STARTING_A_PART_1, "b": 0, "c": 0, "d": 0}
    part_1 = run(program, registers)["a"]
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    registers = {"a": STARTING_A_PART_2, "b": 0, "c": 0, "d": 0}
    part_2 = run(program, registers)["a"]
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
