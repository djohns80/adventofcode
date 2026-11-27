import os

START_PORT = 0


def parse_components(lines):
    components = []
    for line in lines:
        left, right = line.split("/")
        components.append((int(left), int(right)))
    return components


def build_bridges(components, port, used, strength, length):
    # depth-first search over every bridge that can be extended from `port`,
    # yielding (length, strength) for each bridge (including the current one)
    yield length, strength
    for index, (left, right) in enumerate(components):
        if used[index]:
            continue
        if left == port:
            next_port = right
        elif right == port:
            next_port = left
        else:
            continue
        used[index] = True
        yield from build_bridges(
            components, next_port, used, strength + left + right, length + 1
        )
        used[index] = False


def all_bridges(components):
    used = [False] * len(components)
    return build_bridges(components, START_PORT, used, 0, 0)


def strongest_bridge(components, longest=False):
    # with longest=True only the longest bridges count, and the strongest of
    # those wins: tuples compare element by element, so (length, strength)
    # orders by length first and strength second
    best = (0, 0)
    for length, strength in all_bridges(components):
        if not longest:
            length = 0  # ignore the length so only strength matters
        best = max(best, (length, strength))
    return best[1]


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    components = parse_components(lines)

    ##########
    # part 1 #
    ##########
    part_1 = strongest_bridge(components)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = strongest_bridge(components, longest=True)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
