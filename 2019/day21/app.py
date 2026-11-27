import os
from collections import defaultdict, deque

# Jump if there is a hole in any of the next three tiles (A, B or C) and ground
# to land on four tiles away (D). A jump always lands four tiles ahead, so this
# jumps as early as it safely can, before a hole is right in front of the droid.
WALK_SPRINGSCRIPT = [
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
]
WALK_COMMAND = "WALK"

# Same rule as WALK, but also look past the landing tile D: only jump if the
# droid can then either take a step (E is ground) or jump straight again (H is
# ground). Otherwise it waits and jumps later, so it doesn't land in a trap.
RUN_SPRINGSCRIPT = [
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "NOT E T",  # T = E (NOT twice clears what T held before)
    "NOT T T",
    "OR H T",
    "AND T J",
]
RUN_COMMAND = "RUN"

MAX_INSTRUCTIONS = 15  # the springdroid's memory limit


class Intcode:
    """An Intcode computer (2019 days 2, 5, 7 and 9 rules).

    Queue values with `send`, call `run`, then read `outputs`. `run` returns when
    the program halts or when it needs an input that hasn't been queued yet, so it
    can be resumed later for interactive puzzles.
    """

    def __init__(self, program):
        # memory beyond the program reads as 0
        self.memory = defaultdict(int, enumerate(program))
        self.ip = 0
        self.relative_base = 0
        self.inputs = deque()
        self.outputs = []
        self.halted = False

    def send(self, *values):
        self.inputs.extend(values)

    def address(self, offset):
        """Memory address of the parameter at ip + offset, using its mode."""
        mode = self.memory[self.ip] // (10 ** (offset + 1)) % 10
        if mode == 0:  # position
            return self.memory[self.ip + offset]
        if mode == 1:  # immediate
            return self.ip + offset
        return self.relative_base + self.memory[self.ip + offset]  # relative

    def value(self, offset):
        return self.memory[self.address(offset)]

    def run(self):
        while True:
            opcode = self.memory[self.ip] % 100
            match opcode:
                case 1:
                    self.memory[self.address(3)] = self.value(1) + self.value(2)
                    self.ip += 4
                case 2:
                    self.memory[self.address(3)] = self.value(1) * self.value(2)
                    self.ip += 4
                case 3:
                    if not self.inputs:
                        return  # wait for more input
                    self.memory[self.address(1)] = self.inputs.popleft()
                    self.ip += 2
                case 4:
                    self.outputs.append(self.value(1))
                    self.ip += 2
                case 5:
                    self.ip = self.value(2) if self.value(1) != 0 else self.ip + 3
                case 6:
                    self.ip = self.value(2) if self.value(1) == 0 else self.ip + 3
                case 7:
                    self.memory[self.address(3)] = int(self.value(1) < self.value(2))
                    self.ip += 4
                case 8:
                    self.memory[self.address(3)] = int(self.value(1) == self.value(2))
                    self.ip += 4
                case 9:
                    self.relative_base += self.value(1)
                    self.ip += 2
                case 99:
                    self.halted = True
                    return
                case _:
                    raise ValueError(f"unknown opcode {opcode} at {self.ip}")


def send_line(computer, line):
    """Send one line of text to the computer as ASCII codes ending in a newline."""
    for character in line:
        computer.send(ord(character))
    computer.send(ord("\n"))


def run_springscript(program, springscript, command):
    """Program the springdroid, start it with `command` and return the hull damage.

    If the droid falls into space, the ASCII picture of its fall is printed and
    None is returned instead.
    """
    if len(springscript) > MAX_INSTRUCTIONS:
        raise ValueError(f"springscript is longer than {MAX_INSTRUCTIONS} lines")
    computer = Intcode(program)
    for line in springscript:
        send_line(computer, line)
    send_line(computer, command)
    computer.run()

    # a successful survey ends with one value outside the ASCII range
    if computer.outputs and computer.outputs[-1] > 127:
        return computer.outputs[-1]
    print("".join(chr(code) for code in computer.outputs))
    return None


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    program = [int(value) for value in content.split(",")]

    ##########
    # part 1 #
    ##########
    part_1 = run_springscript(program, WALK_SPRINGSCRIPT, WALK_COMMAND)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = run_springscript(program, RUN_SPRINGSCRIPT, RUN_COMMAND)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
