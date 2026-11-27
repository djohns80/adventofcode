import os
import re

# stop the collision simulation after this many ticks in a row without a collision
QUIET_TICKS = 200


def parse_particle(line):
    numbers = []
    for value in re.findall(r"-?\d+", line):
        numbers.append(int(value))
    position = tuple(numbers[0:3])
    velocity = tuple(numbers[3:6])
    acceleration = tuple(numbers[6:9])
    return position, velocity, acceleration


def sign_of_leading_term(coefficients):
    # sign of the first non-zero coefficient (0 if they are all zero)
    for coefficient in coefficients:
        if coefficient > 0:
            return 1
        if coefficient < 0:
            return -1
    return 0


def long_term_distance(particle):
    # Velocity is updated before position, so after t ticks one axis is at
    #   x(t) = p + v*t + a*t*(t+1)/2
    # which, doubled to avoid fractions, is the quadratic
    #   2*x(t) = a*t^2 + (2*v + a)*t + 2*p
    # Once t is large enough the sign of x(t) never changes again: it is the
    # sign of the first non-zero coefficient. So in the long run |x(t)| is that
    # sign times the quadratic, and the Manhattan distance is the sum of those
    # quadratics over the three axes. The returned (t^2, t, constant)
    # coefficients compare in tuple order, so a smaller tuple means the
    # particle ends up closer: acceleration first, then velocity, then position.
    position, velocity, acceleration = particle
    squared_term = 0
    linear_term = 0
    constant_term = 0
    for p, v, a in zip(position, velocity, acceleration):
        coefficients = (a, 2 * v + a, 2 * p)
        sign = sign_of_leading_term(coefficients)
        squared_term += sign * coefficients[0]
        linear_term += sign * coefficients[1]
        constant_term += sign * coefficients[2]
    return squared_term, linear_term, constant_term


def closest_long_term(particles):
    closest_index = 0
    for index, particle in enumerate(particles):
        if long_term_distance(particle) < long_term_distance(particles[closest_index]):
            closest_index = index
    return closest_index


def tick(particle):
    position, velocity, acceleration = particle
    new_velocity = []
    new_position = []
    for p, v, a in zip(position, velocity, acceleration):
        new_velocity.append(v + a)
        new_position.append(p + v + a)
    return tuple(new_position), tuple(new_velocity), acceleration


def count_after_collisions(particles, quiet_ticks):
    # There's no tick at which collisions are guaranteed to be over, so keep
    # simulating until `quiet_ticks` ticks in a row have passed with no
    # collision and assume the remaining particles have separated for good.
    remaining = list(particles)
    ticks_since_collision = 0
    while ticks_since_collision < quiet_ticks:
        particles_at = {}
        for particle in remaining:
            position = particle[0]
            particles_at[position] = particles_at.get(position, 0) + 1
        survivors = []
        for particle in remaining:
            if particles_at[particle[0]] == 1:
                survivors.append(particle)
        if len(survivors) < len(remaining):
            ticks_since_collision = 0
        else:
            ticks_since_collision += 1
        remaining = []
        for particle in survivors:
            remaining.append(tick(particle))
    return len(remaining)


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    particles = []
    for line in lines:
        particles.append(parse_particle(line))

    ##########
    # part 1 #
    ##########
    part_1 = closest_long_term(particles)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = count_after_collisions(particles, QUIET_TICKS)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
