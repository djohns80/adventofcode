import os
from collections import defaultdict, deque

SCAN_SIZE = 50  # scan X and Y from 0 through 49
SQUARE_SIZE = 100  # Santa's ship might fit in a 100x100 square
X_MULTIPLIER = 10000  # answer is X * 10000 + Y


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


def is_pulled(program, x, y):
    """Deploy a drone to (x, y) and report whether the tractor beam pulls it."""
    # the program halts after one answer, so every check needs a fresh computer
    computer = Intcode(program)
    computer.send(x, y)
    computer.run()
    return computer.outputs[0] == 1


def count_pulled_points(program, size):
    """Count the points pulled by the beam in the size x size area at the emitter."""
    count = 0
    for y in range(size):
        for x in range(size):
            if is_pulled(program, x, y):
                count += 1
    return count


def find_square(program, size):
    """Return the top-left corner of the closest size x size square in the beam.

    Walks down the beam's left edge one row at a time. A square whose
    bottom-left corner sits on the left edge fits as soon as its top-right
    corner is in the beam too.
    """
    left = 0
    bottom = size - 1  # the first row that can be the bottom of a square
    while True:
        # the left edge never moves back towards x = 0 as the beam widens
        while not is_pulled(program, left, bottom):
            left += 1
        top = bottom - size + 1
        if is_pulled(program, left + size - 1, top):
            return left, top
        bottom += 1


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
    part_1 = count_pulled_points(program, SCAN_SIZE)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    x, y = find_square(program, SQUARE_SIZE)
    part_2 = x * X_MULTIPLIER + y
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
