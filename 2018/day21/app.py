import os

REGISTER_COUNT = 6
PART_1_REGISTER_0 = 0


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
    # the first line binds the instruction pointer, e.g. "#ip 1"; each other
    # line becomes a tuple like ("seti", 123, 0, 5)
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


def find_register_0_check(instructions):
    # register 0 is only ever read by one eqrr, which compares it with another
    # register; returns that instruction's index and the other register
    for index, (opcode_name, a, b, _) in enumerate(instructions):
        if opcode_name == "eqrr" and a == 0:
            return index, b
        if opcode_name == "eqrr" and b == 0:
            return index, a
    raise ValueError("no eqrr compares against register 0")


def read_hash_constants(instructions):
    # After its bani self-test the program keeps scrambling a "hash" value
    # with a fixed recipe. The recipe's constants sit at fixed places after
    # the only bori:
    #   bori +0: value = previous hash | high_bit
    #   seti +1: hash = seed
    #   bani +2: hash += value & byte_mask (the addr after it does the adding)
    #   bani +4: hash &= hash_mask
    #   muli +5: hash *= multiplier (then masked again by the next bani)
    # Once value is down to a single byte it goes to the eqrr check; otherwise
    # a slow counting loop drops value's lowest byte and the recipe repeats.
    for index, (opcode_name, _, b, _) in enumerate(instructions):
        if opcode_name == "bori":
            high_bit = b
            seed = instructions[index + 1][1]
            byte_mask = instructions[index + 2][2]
            hash_mask = instructions[index + 4][2]
            multiplier = instructions[index + 5][2]
            return high_bit, seed, byte_mask, hash_mask, multiplier
    raise ValueError("no bori found")


def check_values(hash_constants):
    # Yields the value compared with register 0 each time the program reaches
    # the eqrr check. This is the program's loop written out in Python, with
    # the slow counting loop replaced by a division, as running the elfcode
    # itself for thousands of checks would take hours.
    high_bit, seed, byte_mask, hash_mask, multiplier = hash_constants
    hash_value = 0
    while True:
        value = hash_value | high_bit
        hash_value = seed
        while True:
            hash_value = (hash_value + (value & byte_mask)) & hash_mask
            hash_value = (hash_value * multiplier) & hash_mask
            if value <= byte_mask:
                break
            value //= byte_mask + 1
        yield hash_value


def last_new_value(values):
    # each value only depends on the one before it, so once a value repeats
    # the program goes round the same cycle forever and nothing new turns up
    seen = set()
    previous_value = None
    for value in values:
        if value in seen:
            return previous_value
        seen.add(value)
        previous_value = value
    return previous_value


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
    # The program can only halt when that eqrr finds register 0 equal to the
    # other register, so the earliest it can halt is the first time it reaches
    # the check. Run until then: the other register's value at that moment is
    # the register 0 value that halts after the fewest instructions (and, being
    # the only value that halts there, it is also the lowest such value).
    check_index, compared_register = find_register_0_check(instructions)
    registers = run_program(
        ip_register, instructions, PART_1_REGISTER_0, stop_at=check_index
    )
    part_1 = registers[compared_register]
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # The program halts at the first check where register 0 matches, so the
    # value that halts after the most instructions is the one that turns up
    # at the check last, before the values start repeating. (Part 1's answer
    # is the first value of the same sequence.)
    hash_constants = read_hash_constants(instructions)
    part_2 = last_new_value(check_values(hash_constants))
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
