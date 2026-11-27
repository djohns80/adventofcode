import os
import re
from collections import deque
from itertools import combinations

TOP_FLOOR = 3
ELEVATOR_CAPACITY = 2

# positions within a (generator floor, microchip floor) pair
GENERATOR, MICROCHIP = 0, 1

# part 2: an elerium and a dilithium generator and microchip, all on the first floor
EXTRA_PAIRS = [(0, 0), (0, 0)]


def parse_pairs(lines):
    """Return a list of (generator floor, microchip floor), one per element."""
    floors_by_element = {}
    for floor, line in enumerate(lines):
        for element in re.findall(r"(\w+) generator", line):
            floors_by_element.setdefault(element, [None, None])[GENERATOR] = floor
        for element in re.findall(r"(\w+)-compatible microchip", line):
            floors_by_element.setdefault(element, [None, None])[MICROCHIP] = floor
    pairs = []
    for generator_floor, microchip_floor in floors_by_element.values():
        pairs.append((generator_floor, microchip_floor))
    return pairs


def is_safe(pairs):
    generator_floors = set()
    for generator_floor, _ in pairs:
        generator_floors.add(generator_floor)
    for generator_floor, microchip_floor in pairs:
        # a chip away from its own generator is fried by any other generator
        if microchip_floor != generator_floor and microchip_floor in generator_floors:
            return False
    return True


def canonical(elevator, pairs):
    # element names don't matter, only which floors each pair is on, so
    # sorting the pairs makes states that differ only by element name identical
    return elevator, tuple(sorted(pairs))


def next_states(elevator, pairs):
    # items on the elevator's floor, as (pair index, GENERATOR or MICROCHIP)
    items = []
    for index, pair in enumerate(pairs):
        for kind in (GENERATOR, MICROCHIP):
            if pair[kind] == elevator:
                items.append((index, kind))
    loads = []
    for load_size in range(1, ELEVATOR_CAPACITY + 1):
        loads.extend(combinations(items, load_size))

    for new_floor in (elevator - 1, elevator + 1):
        if new_floor < 0 or new_floor > TOP_FLOOR:
            continue
        for load in loads:
            new_pairs = []
            for pair in pairs:
                new_pairs.append(list(pair))
            for index, kind in load:
                new_pairs[index][kind] = new_floor
            new_pairs = [tuple(pair) for pair in new_pairs]
            if is_safe(new_pairs):
                yield canonical(new_floor, new_pairs)


def min_steps(pairs):
    start = canonical(0, pairs)
    goal = canonical(TOP_FLOOR, [(TOP_FLOOR, TOP_FLOOR)] * len(pairs))
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, steps = queue.popleft()
        if state == goal:
            return steps
        for new_state in next_states(*state):
            if new_state not in seen:
                seen.add(new_state)
                queue.append((new_state, steps + 1))
    return None


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    pairs = parse_pairs(lines)

    ##########
    # part 1 #
    ##########
    part_1 = min_steps(pairs)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = min_steps(pairs + EXTRA_PAIRS)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
