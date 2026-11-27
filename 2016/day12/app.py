import os

REGISTER_NAMES = ("a", "b", "c", "d")
PART_2_C_VALUE = 1


def parse_operand(text):
    # registers stay as their name, numbers become ints
    if text in REGISTER_NAMES:
        return text
    return int(text)


def parse_program(lines):
    # each instruction becomes a tuple like ("cpy", 41, "a") or ("inc", "a")
    program = []
    for line in lines:
        words = line.split()
        operands = []
        for word in words[1:]:
            operands.append(parse_operand(word))
        program.append((words[0], *operands))
    return program


def run_program(program, registers):
    registers = dict(registers)

    def value_of(operand):
        if isinstance(operand, str):
            return registers[operand]
        return operand

    pointer = 0
    while 0 <= pointer < len(program):
        instruction = program[pointer]
        opcode = instruction[0]
        if opcode == "cpy":
            registers[instruction[2]] = value_of(instruction[1])
        elif opcode == "inc":
            registers[instruction[1]] += 1
        elif opcode == "dec":
            registers[instruction[1]] -= 1
        elif opcode == "jnz" and value_of(instruction[1]) != 0:
            pointer += value_of(instruction[2])
            continue
        # every other instruction (including a jnz that doesn't jump) moves on by one
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
    program = parse_program(lines)

    ##########
    # part 1 #
    ##########
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    part_1 = run_program(program, registers)["a"]
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    registers = {"a": 0, "b": 0, "c": PART_2_C_VALUE, "d": 0}
    part_2 = run_program(program, registers)["a"]
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
