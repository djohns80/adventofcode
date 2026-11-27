import os
from collections import defaultdict, deque

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4
SCORE_POSITION = (-1, 0)

JOYSTICK_LEFT = -1
JOYSTICK_NEUTRAL = 0
JOYSTICK_RIGHT = 1

QUARTERS_ADDRESS = 0
FREE_PLAY_QUARTERS = 2


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


def draw_outputs(screen, outputs, score):
    """Draw each (x, y, tile id) triple from the outputs onto the screen dict.

    A triple at SCORE_POSITION holds a new score instead of a tile. Returns the
    score after these outputs.
    """
    for index in range(0, len(outputs), 3):
        x, y, value = outputs[index : index + 3]
        if (x, y) == SCORE_POSITION:
            score = value
        else:
            screen[(x, y)] = value
    return score


def count_tiles(screen, tile_id):
    count = 0
    for tile in screen.values():
        if tile == tile_id:
            count += 1
    return count


def find_tile(screen, tile_id):
    for position, tile in screen.items():
        if tile == tile_id:
            return position
    return None


def joystick_towards_ball(screen):
    ball_x, _ = find_tile(screen, BALL)
    paddle_x, _ = find_tile(screen, PADDLE)
    if ball_x < paddle_x:
        return JOYSTICK_LEFT
    if ball_x > paddle_x:
        return JOYSTICK_RIGHT
    return JOYSTICK_NEUTRAL


def play_game(program, quarters=None):
    """Run the arcade game, keeping the paddle under the ball whenever the game
    reads the joystick. Returns the final screen {(x, y): tile id} and score."""
    computer = Intcode(program)
    if quarters is not None:
        computer.memory[QUARTERS_ADDRESS] = quarters
    screen = {}
    score = 0
    while True:
        computer.run()
        score = draw_outputs(screen, computer.outputs, score)
        computer.outputs.clear()
        if computer.halted:
            return screen, score
        computer.send(joystick_towards_ball(screen))


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
    screen, _ = play_game(program)
    part_1 = count_tiles(screen, BLOCK)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    _, part_2 = play_game(program, FREE_PLAY_QUARTERS)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
