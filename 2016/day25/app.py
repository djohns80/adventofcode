import os

# we can't watch the signal forever, so accept it once this many outputs alternate correctly
OUTPUTS_TO_CHECK = 50


def get_value(argument, registers):
    """An argument is either a register name or an integer."""
    if argument in registers:
        return registers[argument]
    return int(argument)


def produces_clock_signal(program, starting_a, outputs_to_check):
    """Run the program and check that it outputs 0, 1, 0, 1, ..."""
    registers = {"a": starting_a, "b": 0, "c": 0, "d": 0}
    expected = 0
    outputs_seen = 0
    pointer = 0
    while 0 <= pointer < len(program):
        match program[pointer]:
            case ["cpy", source, target]:
                registers[target] = get_value(source, registers)
            case ["inc", target]:
                registers[target] += 1
            case ["dec", target]:
                registers[target] -= 1
            case ["jnz", condition, offset]:
                if get_value(condition, registers) != 0:
                    pointer += get_value(offset, registers)
                    continue
            case ["out", source]:
                if get_value(source, registers) != expected:
                    return False
                outputs_seen += 1
                if outputs_seen == outputs_to_check:
                    return True
                expected = 1 - expected
        pointer += 1
    # the program halted, so the signal doesn't repeat forever
    return False


def lowest_clock_signal_start(program, outputs_to_check):
    starting_a = 1
    while not produces_clock_signal(program, starting_a, outputs_to_check):
        starting_a += 1
    return starting_a


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
    part_1 = lowest_clock_signal_start(program, OUTPUTS_TO_CHECK)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # TODO: part 2


if __name__ == "__main__":
    main()
