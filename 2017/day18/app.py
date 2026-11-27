import os
from collections import defaultdict, deque

PROGRAM_IDS = (0, 1)
COUNTED_PROGRAM_ID = 1


def parse_instructions(lines):
    instructions = []
    for line in lines:
        parts = line.split()
        instructions.append((parts[0], parts[1:]))
    return instructions


def get_value(registers, operand):
    # an operand is either a register name (a single letter) or a number
    if operand.isalpha():
        return registers[operand]
    return int(operand)


def apply_instruction(registers, instruction, pointer):
    """Run set/add/mul/mod/jgz and return the next instruction pointer."""
    operation, operands = instruction
    if operation == "jgz":
        if get_value(registers, operands[0]) > 0:
            return pointer + get_value(registers, operands[1])
        return pointer + 1

    register = operands[0]
    value = get_value(registers, operands[1])
    if operation == "set":
        registers[register] = value
    elif operation == "add":
        registers[register] += value
    elif operation == "mul":
        registers[register] *= value
    elif operation == "mod":
        registers[register] %= value
    else:
        raise ValueError(f"unknown instruction: {operation}")
    return pointer + 1


def run_program(instructions, registers, pointer, inbox, outbox, duet=False):
    """Run until a rcv stops the program, or it runs off either end.

    snd always adds a value to the outbox. Without duet, rcv stops the
    program when its value isn't zero (a "recover"). With duet, rcv moves the
    next inbox value into its register, or stops to wait if the inbox is empty.
    Returns the pointer the program stopped at.
    """
    while 0 <= pointer < len(instructions):
        operation, operands = instructions[pointer]
        if operation == "snd":
            outbox.append(get_value(registers, operands[0]))
        elif operation == "rcv":
            if duet:
                if not inbox:
                    return pointer
                registers[operands[0]] = inbox.popleft()
            elif get_value(registers, operands[0]) != 0:
                return pointer
        else:
            pointer = apply_instruction(registers, instructions[pointer], pointer)
            continue
        pointer += 1
    return pointer


def first_recovered_frequency(instructions):
    sounds = []
    pointer = run_program(instructions, defaultdict(int), 0, None, sounds)
    if 0 <= pointer < len(instructions):
        return sounds[-1]
    # the program ended without ever recovering a frequency
    return None


def duet_send_count(instructions, counted_program_id):
    registers = {}
    pointers = {}
    inboxes = {}
    send_counts = {}
    for program_id in PROGRAM_IDS:
        registers[program_id] = defaultdict(int)
        registers[program_id]["p"] = program_id
        pointers[program_id] = 0
        inboxes[program_id] = deque()
        send_counts[program_id] = 0

    while True:
        # run each program in turn until it has to wait for a value (or ends)
        for program_id in PROGRAM_IDS:
            outbox = inboxes[1 - program_id]
            # the other program isn't running, so the outbox only grows
            queued_before = len(outbox)
            pointers[program_id] = run_program(
                instructions,
                registers[program_id],
                pointers[program_id],
                inboxes[program_id],
                outbox,
                duet=True,
            )
            send_counts[program_id] += len(outbox) - queued_before

        # stop once neither program can carry on: each has either ended or is
        # waiting on an empty inbox (a deadlock)
        can_carry_on = False
        for program_id in PROGRAM_IDS:
            still_running = 0 <= pointers[program_id] < len(instructions)
            if still_running and inboxes[program_id]:
                can_carry_on = True
        if not can_carry_on:
            return send_counts[counted_program_id]


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    instructions = parse_instructions(lines)

    ##########
    # part 1 #
    ##########
    part_1 = first_recovered_frequency(instructions)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = duet_send_count(instructions, COUNTED_PROGRAM_ID)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
