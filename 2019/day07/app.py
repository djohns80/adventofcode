import itertools
import os
from collections import defaultdict, deque

SERIES_PHASE_SETTINGS = range(5)
FEEDBACK_PHASE_SETTINGS = range(5, 10)
FIRST_INPUT_SIGNAL = 0


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


def thruster_signal(program, phase_sequence, feedback=False):
    """Signal sent to the thrusters by amplifiers with the given phase settings.

    In feedback mode the last amplifier's output goes back into the first one,
    round and round until the amplifiers halt.
    """
    amplifiers = []
    for phase in phase_sequence:
        amplifier = Intcode(program)  # each amplifier gets its own memory
        amplifier.send(phase)
        amplifiers.append(amplifier)

    signal = FIRST_INPUT_SIGNAL
    while True:
        for amplifier in amplifiers:
            amplifier.send(signal)
            amplifier.run()
            signal = amplifier.outputs.pop()
        if not feedback or amplifiers[-1].halted:
            return signal


def max_thruster_signal(program, phase_settings, feedback=False):
    """Highest thruster signal over every ordering of the phase settings."""
    best_signal = None
    for phase_sequence in itertools.permutations(phase_settings):
        signal = thruster_signal(program, phase_sequence, feedback)
        if best_signal is None or signal > best_signal:
            best_signal = signal
    return best_signal


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
    part_1 = max_thruster_signal(program, SERIES_PHASE_SETTINGS)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = max_thruster_signal(program, FEEDBACK_PHASE_SETTINGS, feedback=True)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
