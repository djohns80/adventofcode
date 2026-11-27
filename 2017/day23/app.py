import os

REGISTER_NAMES = "abcdefgh"
DEBUG_SWITCH_ON = 1  # part 2: register a starts at 1
# the first instruction of the program's main loop, right after its setup code
MAIN_LOOP_START = ("set", "f", "1")


def parse_program(lines):
    program = []
    for line in lines:
        operation, x, y = line.split()
        program.append((operation, x, y))
    return program


def start_registers(a_value):
    registers = {}
    for name in REGISTER_NAMES:
        registers[name] = 0
    registers["a"] = a_value
    return registers


def value_of(operand, registers):
    # an operand is either a register name or an integer literal
    if operand in registers:
        return registers[operand]
    return int(operand)


def run(program, registers, stop_at=None):
    # runs until the instruction pointer leaves the program (or reaches the
    # instruction index `stop_at`) and returns the final registers and how
    # many times mul was executed
    registers = dict(registers)  # work on a copy so the caller's dict is unchanged
    pointer = 0
    mul_count = 0
    while 0 <= pointer < len(program) and pointer != stop_at:
        operation, x, y = program[pointer]
        if operation == "set":
            registers[x] = value_of(y, registers)
        elif operation == "sub":
            registers[x] -= value_of(y, registers)
        elif operation == "mul":
            registers[x] *= value_of(y, registers)
            mul_count += 1
        elif operation == "jnz" and value_of(x, registers) != 0:
            pointer += value_of(y, registers)
            continue
        pointer += 1
    return registers, mul_count


def is_prime(number):
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def final_h(program, a_value):
    # Translated by hand, the program is:
    #
    #   setup: compute b and c from a (with a = 1 they become much larger)
    #   loop:  f = 1
    #          for d in 2 .. b - 1:
    #              for e in 2 .. b - 1:
    #                  if d * e == b: f = 0
    #          if f == 0: h += 1
    #          if b == c: stop
    #          b += step  (the last "sub b" instruction, which subtracts -step)
    #
    # So h ends up as the number of non-prime values of b from b to c
    # inclusive, going up by step each time. The two inner loops take about b^2
    # instructions per value of b, far too slow to simulate. Instead: run only
    # the setup code with the interpreter to get b and c, read the step from
    # the program, and count the non-primes directly.
    registers, _ = run(
        program, start_registers(a_value), stop_at=program.index(MAIN_LOOP_START)
    )
    step = 0
    for operation, x, y in program:
        if operation == "sub" and x == "b":
            step = -int(y)
    non_primes = 0
    for b in range(registers["b"], registers["c"] + 1, step):
        if not is_prime(b):
            non_primes += 1
    return non_primes


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
    _, mul_count = run(program, start_registers(0))
    part_1 = mul_count
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = final_h(program, DEBUG_SWITCH_ON)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
