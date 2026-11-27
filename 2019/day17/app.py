import os
from collections import defaultdict, deque

# characters in the camera view that are scaffold (the robot is always on one)
SCAFFOLD_TILES = "#^v<>"
# (dx, dy) the robot faces for each of its characters, with y increasing downwards
ROBOT_DIRECTIONS = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}

WAKE_UP_ADDRESS = 0
WAKE_UP_VALUE = 2
FUNCTION_NAMES = "ABC"
MAX_ROUTINE_LENGTH = 20  # characters, not counting the newline
VIDEO_FEED = "n"


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


def decode_ascii(outputs):
    return "".join(chr(code) for code in outputs)


def encode_ascii(text):
    return [ord(character) for character in text]


def camera_view(program):
    """Run the ASCII program and return the camera image as a list of rows."""
    computer = Intcode(program)
    computer.run()
    return decode_ascii(computer.outputs).strip().splitlines()


def is_scaffold(rows, x, y):
    if y < 0 or y >= len(rows) or x < 0 or x >= len(rows[y]):
        return False
    return rows[y][x] in SCAFFOLD_TILES


def find_intersections(rows):
    """Positions (x, y) of scaffold whose four neighbours are all scaffold too."""
    intersections = []
    for y, row in enumerate(rows):
        for x in range(len(row)):
            neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            if is_scaffold(rows, x, y) and all(
                is_scaffold(rows, nx, ny) for nx, ny in neighbours
            ):
                intersections.append((x, y))
    return intersections


def sum_alignment_parameters(intersections):
    total = 0
    for x, y in intersections:
        total += x * y
    return total


def find_robot(rows):
    """The robot's position (x, y) and the (dx, dy) it is facing."""
    for y, row in enumerate(rows):
        for x, tile in enumerate(row):
            if tile in ROBOT_DIRECTIONS:
                return (x, y), ROBOT_DIRECTIONS[tile]
    return None


def scaffold_path(rows):
    """The robot's route along the whole scaffold, as steps like "R,8".

    It goes straight across intersections and only turns at corners, so it
    stops at the far end of the scaffold.
    """
    (x, y), (dx, dy) = find_robot(rows)
    steps = []
    while True:
        # with y increasing downwards, turning left takes (dx, dy) to (dy, -dx)
        left = (dy, -dx)
        right = (-dy, dx)
        if is_scaffold(rows, x + left[0], y + left[1]):
            turn = "L"
            dx, dy = left
        elif is_scaffold(rows, x + right[0], y + right[1]):
            turn = "R"
            dx, dy = right
        else:
            return steps
        distance = 0
        while is_scaffold(rows, x + dx, y + dy):
            x += dx
            y += dy
            distance += 1
        steps.append(f"{turn},{distance}")


def compress_path(steps, routine=(), functions=()):
    """Depth-first search for a main routine and movement functions that make up
    the steps, each at most MAX_ROUTINE_LENGTH characters long.

    Returns (main routine, [function, ...]) as text, or None if there isn't one.
    """
    if len(",".join(routine)) > MAX_ROUTINE_LENGTH:
        return None
    if not steps:
        return ",".join(routine), [",".join(function) for function in functions]

    # call a function we already have if the path carries on with its steps
    for name, function in zip(FUNCTION_NAMES, functions):
        if steps[: len(function)] == function:
            result = compress_path(steps[len(function) :], routine + (name,), functions)
            if result is not None:
                return result

    # or make the next few steps into a new function
    if len(functions) < len(FUNCTION_NAMES):
        name = FUNCTION_NAMES[len(functions)]
        for length in range(1, len(steps) + 1):
            function = steps[:length]
            if len(",".join(function)) > MAX_ROUTINE_LENGTH:
                break
            result = compress_path(
                steps[length:], routine + (name,), functions + (function,)
            )
            if result is not None:
                return result
    return None


def collect_dust(program, main_routine, functions):
    """Wake the robot, give it the movement rules and return the dust it reports."""
    computer = Intcode(program)
    computer.memory[WAKE_UP_ADDRESS] = WAKE_UP_VALUE
    # functions the main routine doesn't use are left empty
    padded_functions = functions + [""] * (len(FUNCTION_NAMES) - len(functions))
    for line in [main_routine, *padded_functions, VIDEO_FEED]:
        computer.send(*encode_ascii(line + "\n"))
    computer.run()
    # everything before the final, non-ASCII, value is the camera and prompts
    return computer.outputs[-1]


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
    rows = camera_view(program)
    part_1 = sum_alignment_parameters(find_intersections(rows))
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    main_routine, functions = compress_path(scaffold_path(rows))
    part_2 = collect_dust(program, main_routine, functions)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
