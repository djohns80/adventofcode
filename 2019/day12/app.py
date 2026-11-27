import math
import os

STEPS = 1000


def parse_positions(lines):
    """Turn lines like '<x=-1, y=0, z=2>' into lists of [x, y, z]."""
    positions = []
    for line in lines:
        coordinates = []
        for part in line.strip("<>").split(","):
            coordinates.append(int(part.split("=")[1]))
        positions.append(coordinates)
    return positions


def initial_state(start_positions):
    """Return fresh position lists and all-zero velocity lists."""
    positions = []
    velocities = []
    for coordinates in start_positions:
        positions.append(list(coordinates))
        velocities.append([0] * len(coordinates))
    return positions, velocities


def apply_step(positions, velocities, axes):
    """Advance every moon by one time step on the given axes, in place."""
    moon_count = len(positions)

    # gravity: each pair of moons is pulled together by 1 on every axis
    for first in range(moon_count):
        for second in range(first + 1, moon_count):
            for axis in axes:
                if positions[first][axis] < positions[second][axis]:
                    velocities[first][axis] += 1
                    velocities[second][axis] -= 1
                elif positions[first][axis] > positions[second][axis]:
                    velocities[first][axis] -= 1
                    velocities[second][axis] += 1

    # velocity: move each moon
    for moon in range(moon_count):
        for axis in axes:
            positions[moon][axis] += velocities[moon][axis]


def simulate(start_positions, steps):
    """Return the positions and velocities after the given number of steps."""
    positions, velocities = initial_state(start_positions)
    all_axes = range(len(start_positions[0]))
    for _ in range(steps):
        apply_step(positions, velocities, all_axes)
    return positions, velocities


def total_energy(positions, velocities):
    total = 0
    for position, velocity in zip(positions, velocities):
        potential = 0
        for value in position:
            potential += abs(value)
        kinetic = 0
        for value in velocity:
            kinetic += abs(value)
        total += potential * kinetic
    return total


def steps_until_repeat(start_positions):
    """Return the number of steps before the moons first repeat a previous state.

    Gravity on one axis only depends on positions on that axis, so the x, y and
    z axes move independently. Each step can also be run backwards, so the first
    repeated state is always the starting one. That means each axis cycles back
    to its start on its own period, and the whole system repeats once every axis
    does at the same time: the lowest common multiple of the axis periods.
    """
    _, zero_velocities = initial_state(start_positions)
    periods = []
    for axis in range(len(start_positions[0])):
        positions, velocities = initial_state(start_positions)
        steps = 0
        while True:
            apply_step(positions, velocities, [axis])
            steps += 1
            # the other axes are never moved, so comparing whole lists is enough
            if positions == start_positions and velocities == zero_velocities:
                break
        periods.append(steps)
    return math.lcm(*periods)


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    start_positions = parse_positions(lines)

    ##########
    # part 1 #
    ##########
    positions, velocities = simulate(start_positions, STEPS)
    part_1 = total_energy(positions, velocities)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = steps_until_repeat(start_positions)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
