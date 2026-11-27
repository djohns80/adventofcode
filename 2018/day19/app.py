import os

REGISTER_COUNT = 6
PART_1_REGISTER_0 = 0
PART_2_REGISTER_0 = 1


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


def parse_program(lines):
    # the first line binds the instruction pointer, e.g. "#ip 5"; each other
    # line becomes a tuple like ("addi", 5, 16, 5)
    ip_register = int(lines[0].split()[1])
    instructions = []
    for line in lines[1:]:
        opcode_name, a, b, c = line.split()
        instructions.append((opcode_name, int(a), int(b), int(c)))
    return ip_register, instructions


def run_program(ip_register, instructions, register_0, stop_at=None):
    # runs until the program halts, or until it is about to execute the
    # instruction at index stop_at
    registers = [0] * REGISTER_COUNT
    registers[0] = register_0
    ip = 0
    while 0 <= ip < len(instructions) and ip != stop_at:
        opcode_name, a, b, c = instructions[ip]
        # the bound register holds the instruction pointer while each instruction
        # runs, and any change the instruction makes to it acts as a jump
        registers[ip_register] = ip
        execute(opcode_name, a, b, c, registers)
        ip = registers[ip_register] + 1
    return registers


def sum_of_divisors(number):
    total = 0
    divisor = 1
    while divisor * divisor <= number:
        if number % divisor == 0:
            # divisors come in pairs, divisor and number // divisor
            total += divisor
            if divisor != number // divisor:
                total += number // divisor
        divisor += 1
    return total


def background_process_result(ip_register, instructions, register_0):
    # Running the whole program is far too slow when register 0 starts at 1.
    # Its first instruction jumps to a setup section at the end, which builds a
    # number (much bigger when register 0 is 1) and then jumps back to
    # instruction 1. From there the main loop tries every pair of factors up to
    # that number and adds the first one to register 0 whenever the pair
    # multiplies to it, so register 0 ends up as the sum of the number's
    # divisors. So only run the setup, take the number from the registers (it
    # is the largest value in them) and add up its divisors directly.
    registers = run_program(ip_register, instructions, register_0, stop_at=1)
    return sum_of_divisors(max(registers))


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    ip_register, instructions = parse_program(lines)

    ##########
    # part 1 #
    ##########
    part_1 = background_process_result(ip_register, instructions, PART_1_REGISTER_0)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = background_process_result(ip_register, instructions, PART_2_REGISTER_0)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
