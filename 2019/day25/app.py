import copy
import itertools
import os
import re
from collections import defaultdict, deque

# a normal reply is a few hundred characters; far more means a runaway program
MAX_OUTPUT_LENGTH = 10_000


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


class RunawayOutputError(Exception):
    """The program kept printing instead of asking for the next command."""


class LimitedOutput(list):
    """An output list that stops a runaway program once it grows too long."""

    def append(self, value):
        super().append(value)
        if len(self) > MAX_OUTPUT_LENGTH:
            raise RunawayOutputError


def run_command(computer, command):
    """Send one line of text (None sends nothing) and return the text printed back."""
    computer.outputs = LimitedOutput()
    if command is not None:
        for character in command + "\n":
            computer.send(ord(character))
    computer.run()
    return "".join(chr(code) for code in computer.outputs)


def parse_room(text):
    """Return the name, doors and items of the last room described in the text.

    The name is None if the text doesn't describe a room at all.
    """
    name = None
    doors = []
    items = []
    current_list = None
    for line in text.splitlines():
        if line.startswith("== "):
            # a new room description; any earlier one in the text is replaced
            name = line.strip("= ")
            doors = []
            items = []
            current_list = None
        elif line == "Doors here lead:":
            current_list = doors
        elif line == "Items here:":
            current_list = items
        elif line.startswith("- ") and current_list is not None:
            current_list.append(line[2:])
        else:
            current_list = None
    return name, doors, items


def explore(computer, start_text):
    """Map the ship by trying every door, each from a copy of the computer.

    Returns the rooms (name -> doors, neighbours, items and a copy of the
    computer standing there), the start room's name, and the room and door
    where the droid gets sent straight back (the pressure-sensitive floor).
    """
    start, doors, items = parse_room(start_text)
    rooms = {
        start: {
            "doors": doors,
            "neighbours": {},
            "items": items,
            "computer": copy.deepcopy(computer),
        }
    }
    floor_room = None
    floor_door = None
    queue = deque([start])
    while queue:
        name = queue.popleft()
        room = rooms[name]
        for door in room["doors"]:
            explorer = copy.deepcopy(room["computer"])
            next_name, next_doors, next_items = parse_room(run_command(explorer, door))
            if next_name == name:
                # the floor weighed the droid and pushed it back to this room
                floor_room = name
                floor_door = door
                continue
            room["neighbours"][door] = next_name
            if next_name not in rooms:
                rooms[next_name] = {
                    "doors": next_doors,
                    "neighbours": {},
                    "items": next_items,
                    "computer": explorer,
                }
                queue.append(next_name)
    return rooms, start, floor_room, floor_door


def is_safe_item(computer, item, door):
    """Take the item on a copy of the computer and check the droid still works.

    Traps end the game, make the program print forever, or stop the droid
    moving, so after taking the item the droid must still be able to walk
    through a door into a room.
    """
    trial = copy.deepcopy(computer)
    try:
        run_command(trial, f"take {item}")
        if trial.halted:
            return False
        reply = run_command(trial, door)
    except RunawayOutputError:
        return False
    name, _, _ = parse_room(reply)
    return not trial.halted and name is not None


def find_safe_items(rooms):
    """Return {room name: [items that are safe to carry]}."""
    safe_items = {}
    for name, room in rooms.items():
        for item in room["items"]:
            if is_safe_item(room["computer"], item, room["doors"][0]):
                safe_items.setdefault(name, []).append(item)
    return safe_items


def find_path(rooms, start, goal):
    """Return the shortest list of doors leading from start to goal."""
    paths = {start: []}
    queue = deque([start])
    while queue:
        name = queue.popleft()
        if name == goal:
            return paths[name]
        for door, neighbour in rooms[name]["neighbours"].items():
            if neighbour not in paths:
                paths[neighbour] = paths[name] + [door]
                queue.append(neighbour)
    raise ValueError(f"no path from {start} to {goal}")


def walk(computer, rooms, start, goal):
    """Move the droid from start to goal."""
    for door in find_path(rooms, start, goal):
        run_command(computer, door)


def collect_items(computer, rooms, start, items_by_room):
    """Visit each room in turn taking the listed items; return the final room."""
    position = start
    for name, items in items_by_room.items():
        walk(computer, rooms, position, name)
        position = name
        for item in items:
            run_command(computer, f"take {item}")
    return position


def pass_pressure_floor(computer, items, floor_room, floor_door):
    """Carry each subset of the items onto the floor until one weighs right.

    The droid must start in floor_room carrying all the items. Returns the
    text printed when the floor lets the droid through.
    """
    carried = set(items)
    for size in range(len(items) + 1):
        for subset in itertools.combinations(items, size):
            wanted = set(subset)
            for item in sorted(carried - wanted):
                run_command(computer, f"drop {item}")
            for item in sorted(wanted - carried):
                run_command(computer, f"take {item}")
            carried = wanted
            reply = run_command(computer, floor_door)
            name, _, _ = parse_room(reply)
            if computer.halted or name != floor_room:
                return reply
    raise RuntimeError("no combination of items has the right weight")


def find_airlock_password(program):
    """Explore the ship, gather the safe items and get past the floor."""
    computer = Intcode(program)
    start_text = run_command(computer, None)
    rooms, start, floor_room, floor_door = explore(computer, start_text)

    safe_items = find_safe_items(rooms)
    position = collect_items(computer, rooms, start, safe_items)
    walk(computer, rooms, position, floor_room)

    all_items = []
    for items in safe_items.values():
        all_items.extend(items)
    reply = pass_pressure_floor(computer, all_items, floor_room, floor_door)

    # the password is the only number in Santa's final message
    final_message = reply.strip().splitlines()[-1]
    return int(re.search(r"\d+", final_message).group())


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
    part_1 = find_airlock_password(program)
    print("part 1:", part_1)


if __name__ == "__main__":
    main()
