import os
from collections import defaultdict, deque

BLACK = 0
WHITE = 1
TURN_LEFT = 0
TURN_RIGHT = 1
# (dx, dy) in clockwise order, with y increasing downwards; the robot starts facing up
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


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


def paint_hull(program, starting_colour):
    """Run the painting robot on a hull where only its starting panel may be white.

    Returns (colours, painted): the colour of every panel the robot has seen or
    painted (any other panel is black) and the set of panels painted at least once.
    """
    position = (0, 0)
    direction = 0  # index into DIRECTIONS
    colours = {position: starting_colour}
    painted = set()
    computer = Intcode(program)
    while not computer.halted:
        computer.send(colours.get(position, BLACK))
        computer.run()
        # each camera input is answered with a colour to paint and a way to turn
        paint_colour, turn = computer.outputs
        computer.outputs.clear()

        colours[position] = paint_colour
        painted.add(position)
        if turn == TURN_RIGHT:
            direction = (direction + 1) % len(DIRECTIONS)
        else:
            direction = (direction - 1) % len(DIRECTIONS)
        dx, dy = DIRECTIONS[direction]
        position = (position[0] + dx, position[1] + dy)
    return colours, painted


def draw_hull(colours):
    """Rows of text showing white panels as # and black panels as spaces."""
    white_panels = []
    for position, colour in colours.items():
        if colour == WHITE:
            white_panels.append(position)
    min_x = min(x for x, _ in white_panels)
    max_x = max(x for x, _ in white_panels)
    min_y = min(y for _, y in white_panels)
    max_y = max(y for _, y in white_panels)

    rows = []
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            row += "#" if colours.get((x, y), BLACK) == WHITE else " "
        rows.append(row)
    return rows


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
    _, painted = paint_hull(program, BLACK)
    part_1 = len(painted)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    colours, _ = paint_hull(program, WHITE)
    part_2 = "\n".join(draw_hull(colours))
    print("part 2:")
    print(part_2)


if __name__ == "__main__":
    main()
