import os
from collections import defaultdict, deque

BOOST_TEST_MODE = 1
SENSOR_BOOST_MODE = 2


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


def run_boost(program, mode):
    """Run BOOST with the given mode as its input and return everything it outputs."""
    computer = Intcode(program)
    computer.send(mode)
    computer.run()
    return computer.outputs


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
    outputs = run_boost(program, BOOST_TEST_MODE)
    # anything before the keycode is a malfunctioning opcode
    if len(outputs) > 1:
        print("malfunctioning opcodes:", outputs[:-1])
    part_1 = outputs[-1]
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # sensor boost mode outputs a single value: the distress signal's coordinates
    part_2 = run_boost(program, SENSOR_BOOST_MODE)[0]
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
