import os

OPCODE_NAMES = (
    "addr",
    "addi",
    "mulr",
    "muli",
    "banr",
    "bani",
    "borr",
    "bori",
    "setr",
    "seti",
    "gtir",
    "gtri",
    "gtrr",
    "eqir",
    "eqri",
    "eqrr",
)
MIN_MATCHING_OPCODES = 3
REGISTER_COUNT = 4


def execute(opcode_name, a, b, c, registers):
    # updates registers in place; in the opcode names "r" means an input is read
    # from that register and "i" means it is used as a plain value
    match opcode_name:
        case "addr":
            registers[c] = registers[a] + registers[b]
        case "addi":
            registers[c] = registers[a] + b
        case "mulr":
            registers[c] = registers[a] * registers[b]
        case "muli":
            registers[c] = registers[a] * b
        case "banr":
            registers[c] = registers[a] & registers[b]
        case "bani":
            registers[c] = registers[a] & b
        case "borr":
            registers[c] = registers[a] | registers[b]
        case "bori":
            registers[c] = registers[a] | b
        case "setr":
            registers[c] = registers[a]
        case "seti":
            registers[c] = a
        case "gtir":
            registers[c] = 1 if a > registers[b] else 0
        case "gtri":
            registers[c] = 1 if registers[a] > b else 0
        case "gtrr":
            registers[c] = 1 if registers[a] > registers[b] else 0
        case "eqir":
            registers[c] = 1 if a == registers[b] else 0
        case "eqri":
            registers[c] = 1 if registers[a] == b else 0
        case "eqrr":
            registers[c] = 1 if registers[a] == registers[b] else 0
        case _:
            raise ValueError(f"unknown opcode {opcode_name}")


def parse_registers(line):
    # "Before: [3, 2, 1, 1]" becomes [3, 2, 1, 1]
    inside_brackets = line[line.index("[") + 1 : line.index("]")]
    registers = []
    for value in inside_brackets.split(", "):
        registers.append(int(value))
    return registers


def parse_instruction(line):
    # "9 2 1 2" becomes [9, 2, 1, 2]
    instruction = []
    for value in line.split():
        instruction.append(int(value))
    return instruction


def parse_input(lines):
    # each sample is a Before line, an instruction line, an After line and a
    # blank line; the test program follows after the last sample
    samples = []
    index = 0
    while index < len(lines) and lines[index].startswith("Before:"):
        before = parse_registers(lines[index])
        instruction = parse_instruction(lines[index + 1])
        after = parse_registers(lines[index + 2])
        samples.append((before, instruction, after))
        index += 4
    program = []
    for line in lines[index:]:
        if line:
            program.append(parse_instruction(line))
    return samples, program


def matching_opcodes(before, instruction, after):
    # the opcode number is what we're trying to work out, so only A, B and C are used
    _, a, b, c = instruction
    matches = set()
    for opcode_name in OPCODE_NAMES:
        registers = list(before)
        execute(opcode_name, a, b, c, registers)
        if registers == after:
            matches.add(opcode_name)
    return matches


def deduce_opcode_names(samples):
    # each number starts out as whatever its first sample allows, and every
    # further sample for that number narrows it down
    candidates = {}
    for before, instruction, after in samples:
        opcode_number = instruction[0]
        matches = matching_opcodes(before, instruction, after)
        if opcode_number in candidates:
            candidates[opcode_number] &= matches
        else:
            candidates[opcode_number] = matches
    # then repeatedly settle a number that has only one name left, and rule
    # that name out for all the other numbers
    names_by_number = {}
    while candidates:
        solved_number = None
        for opcode_number, names in candidates.items():
            if len(names) == 1:
                solved_number = opcode_number
        if solved_number is None:
            raise ValueError("the samples don't pin down every opcode")
        last_name_left = candidates.pop(solved_number)
        solved_name = last_name_left.pop()
        names_by_number[solved_number] = solved_name
        for names in candidates.values():
            names.discard(solved_name)
    return names_by_number


def run_test_program(program, names_by_number):
    registers = [0] * REGISTER_COUNT
    for opcode_number, a, b, c in program:
        execute(names_by_number[opcode_number], a, b, c, registers)
    return registers


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    samples, program = parse_input(lines)

    ##########
    # part 1 #
    ##########
    part_1 = 0
    for before, instruction, after in samples:
        if len(matching_opcodes(before, instruction, after)) >= MIN_MATCHING_OPCODES:
            part_1 += 1
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    names_by_number = deduce_opcode_names(samples)
    part_2 = run_test_program(program, names_by_number)[0]
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
