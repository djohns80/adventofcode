import os

INSERTIONS = 2017
ANGRY_INSERTIONS = 50_000_000


def next_position(position, steps, length):
    # step forward around the circle, then insert just after where we stopped
    return (position + steps) % length + 1


def spinlock(steps, insertions):
    buffer = [0]
    position = 0
    for value in range(1, insertions + 1):
        position = next_position(position, steps, len(buffer))
        buffer.insert(position, value)
    return buffer, position


def value_after_last_insert(steps, insertions):
    buffer, position = spinlock(steps, insertions)
    return buffer[(position + 1) % len(buffer)]


def value_after_zero(steps, insertions):
    # nothing is ever inserted before 0, so 0 stays at index 0 and the value
    # after it is simply the last value inserted at index 1; that means only
    # the current position and the buffer length need tracking, not the buffer
    position = 0
    value = 0  # the last value inserted; the buffer holds value + 1 values
    after_zero = None
    while value < insertions:
        length = value + 1
        # until the position wraps around past the end, each insert just moves
        # it forward by steps + 1, well away from index 1, so all of those
        # inserts can be skipped over in one go
        inserts_before_wrap = (length - position - 1) // steps
        inserts_before_wrap = min(inserts_before_wrap, insertions - value)
        position += inserts_before_wrap * (steps + 1)
        value += inserts_before_wrap
        if value == insertions:
            break
        # this insert wraps around, so it might land at index 1
        position = next_position(position, steps, value + 1)
        value += 1
        if position == 1:
            after_zero = value
    return after_zero


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    steps = int(content.strip())

    ##########
    # part 1 #
    ##########
    part_1 = value_after_last_insert(steps, INSERTIONS)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = value_after_zero(steps, ANGRY_INSERTIONS)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
