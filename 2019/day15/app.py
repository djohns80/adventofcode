import os
from collections import defaultdict, deque

# movement commands and the (dx, dy) step each one makes, with y increasing south
NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
STEPS = {NORTH: (0, -1), SOUTH: (0, 1), WEST: (-1, 0), EAST: (1, 0)}
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}

# status codes, which also say what is at the position the droid tried to enter
WALL = 0
OPEN = 1
OXYGEN_SYSTEM = 2

START = (0, 0)


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


def step(position, command):
    dx, dy = STEPS[command]
    return (position[0] + dx, position[1] + dy)


def move(computer, command):
    """Send one movement command to the droid and return its status code."""
    computer.send(command)
    computer.run()
    return computer.outputs.pop()


def explore(computer, position, area):
    """Depth-first search from the droid's position, recording in area the status
    of every position it tries. The droid finishes back where it started."""
    for command in STEPS:
        target = step(position, command)
        if target in area:
            continue
        status = move(computer, command)
        area[target] = status
        if status != WALL:
            explore(computer, target, area)
            move(computer, OPPOSITE[command])  # backtrack


def map_area(program):
    """Explore the whole area with the droid and return {position: status}."""
    area = {START: OPEN}
    explore(Intcode(program), START, area)
    return area


def find_oxygen_system(area):
    for position, status in area.items():
        if status == OXYGEN_SYSTEM:
            return position
    return None


def shortest_distances(area, source):
    """Breadth-first search: fewest moves from source to every reachable position."""
    distances = {source: 0}
    queue = deque([source])
    while queue:
        position = queue.popleft()
        for command in STEPS:
            neighbour = step(position, command)
            if area.get(neighbour, WALL) != WALL and neighbour not in distances:
                distances[neighbour] = distances[position] + 1
                queue.append(neighbour)
    return distances


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
    area = map_area(program)
    oxygen_system = find_oxygen_system(area)
    distances = shortest_distances(area, START)
    part_1 = distances[oxygen_system]
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # oxygen spreads one position a minute, so the furthest position fills last
    part_2 = max(shortest_distances(area, oxygen_system).values())
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
