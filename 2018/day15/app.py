import os
from dataclasses import dataclass

ELF = "E"
GOBLIN = "G"
WALL = "#"
ATTACK_POWER = 3
STARTING_HIT_POINTS = 200
MIN_BOOSTED_ATTACK_POWER = 4  # part 2: the lowest elf attack power to try
# up, left, right, down: the order adjacent squares come in reading order
NEIGHBOUR_OFFSETS = ((-1, 0), (0, -1), (0, 1), (1, 0))


@dataclass
class Unit:
    kind: str
    position: tuple  # (row, col), so sorting positions gives reading order
    attack_power: int
    hit_points: int = STARTING_HIT_POINTS

    @property
    def alive(self):
        return self.hit_points > 0


def parse_cave(lines):
    """Return the set of open squares (including those units stand on) and each unit's (kind, position)."""
    open_squares = set()
    unit_starts = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == WALL:
                continue
            open_squares.add((row, col))
            if char in (ELF, GOBLIN):
                unit_starts.append((char, (row, col)))
    return open_squares, unit_starts


def neighbours(position):
    """Adjacent squares in reading order."""
    row, col = position
    result = []
    for d_row, d_col in NEIGHBOUR_OFFSETS:
        result.append((row + d_row, col + d_col))
    return result


def nearest_square(start, goals, open_squares, occupied):
    """
    Breadth-first search outwards from start, one distance at a time, without
    passing through walls or units. Returns the closest goal square (ties broken
    by reading order), or None if no goal can be reached. Stopping at the first
    distance with a goal keeps the search small, which matters in part 2.
    """
    seen = {start}
    frontier = [start]
    while frontier:
        found = []
        for square in frontier:
            if square in goals:
                found.append(square)
        if found:
            return min(found)
        next_frontier = []
        for square in frontier:
            for next_square in neighbours(square):
                if next_square in seen:
                    continue
                if next_square not in open_squares or next_square in occupied:
                    continue
                seen.add(next_square)
                next_frontier.append(next_square)
        frontier = next_frontier
    return None


def choose_step(unit, enemies, open_squares, occupied):
    """The square the unit should step into this turn, or None if it can't reach any enemy."""
    in_range = set()
    for enemy in enemies:
        for square in neighbours(enemy.position):
            if square in open_squares and square not in occupied:
                in_range.add(square)
    destination = nearest_square(unit.position, in_range, open_squares, occupied)
    if destination is None:
        return None

    # searching back from the destination, the nearest of the unit's free
    # neighbours is the first step of a shortest path; if several shortest paths
    # exist, the tie-break picks the step first in reading order
    free_neighbours = set()
    for square in neighbours(unit.position):
        if square in open_squares and square not in occupied:
            free_neighbours.add(square)
    return nearest_square(destination, free_neighbours, open_squares, occupied)


def adjacent_enemies(unit, enemies):
    adjacent_squares = neighbours(unit.position)
    result = []
    for enemy in enemies:
        if enemy.alive and enemy.position in adjacent_squares:
            result.append(enemy)
    return result


def take_turn(unit, units, open_squares):
    """
    Move (if not already next to an enemy) and then attack.
    Returns False if there were no enemies left, meaning combat is over.
    """
    enemies = []
    for other in units:
        if other.alive and other.kind != unit.kind:
            enemies.append(other)
    if not enemies:
        return False

    if not adjacent_enemies(unit, enemies):
        occupied = set()
        for other in units:
            if other.alive:
                occupied.add(other.position)
        step = choose_step(unit, enemies, open_squares, occupied)
        if step is not None:
            unit.position = step

    targets = adjacent_enemies(unit, enemies)
    if targets:
        # fewest hit points first, ties broken by reading order
        target = min(targets, key=lambda enemy: (enemy.hit_points, enemy.position))
        target.hit_points -= unit.attack_power
    return True


def any_elf_died(units):
    for unit in units:
        if unit.kind == ELF and not unit.alive:
            return True
    return False


def run_combat(open_squares, unit_starts, elf_attack_power, stop_on_elf_death=False):
    """
    Fight until a unit finds no enemies on its turn (or, with stop_on_elf_death,
    as soon as an elf dies, since that fight is already lost).
    Returns the number of full rounds completed and the units (alive and dead).
    """
    units = []
    for kind, position in unit_starts:
        attack_power = elf_attack_power if kind == ELF else ATTACK_POWER
        units.append(Unit(kind, position, attack_power))

    full_rounds = 0
    while True:
        # turn order is fixed by positions at the start of the round
        for unit in sorted(units, key=lambda u: u.position):
            if not unit.alive:
                continue
            if not take_turn(unit, units, open_squares):
                return full_rounds, units
            if stop_on_elf_death and any_elf_died(units):
                return full_rounds, units
        full_rounds += 1


def lowest_flawless_outcome(open_squares, unit_starts):
    """Outcome of the fight with the lowest elf attack power at which no elf dies."""
    elf_attack_power = MIN_BOOSTED_ATTACK_POWER
    while True:
        full_rounds, units = run_combat(
            open_squares, unit_starts, elf_attack_power, stop_on_elf_death=True
        )
        if not any_elf_died(units):
            return combat_outcome(full_rounds, units)
        elf_attack_power += 1


def combat_outcome(full_rounds, units):
    remaining_hit_points = 0
    for unit in units:
        if unit.alive:
            remaining_hit_points += unit.hit_points
    return full_rounds * remaining_hit_points


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    open_squares, unit_starts = parse_cave(lines)

    ##########
    # part 1 #
    ##########
    full_rounds, units = run_combat(open_squares, unit_starts, ATTACK_POWER)
    part_1 = combat_outcome(full_rounds, units)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = lowest_flawless_outcome(open_squares, unit_starts)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
