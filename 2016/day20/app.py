import os

MAX_IP = 4294967295


def allowed_ranges(blocked_ranges, max_ip):
    """Return the (first, last) ranges of IPs not covered by any blocked range, in order."""
    allowed = []
    candidate = 0  # lowest IP not yet known to be blocked
    for start, end in sorted(blocked_ranges):
        if start > candidate:
            # there is a gap before this range, so those IPs are allowed
            allowed.append((candidate, start - 1))
        candidate = max(candidate, end + 1)
    if candidate <= max_ip:
        # everything after the last blocked range is allowed too
        allowed.append((candidate, max_ip))
    return allowed


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    blocked_ranges = []
    for line in lines:
        start, end = line.split("-")
        blocked_ranges.append((int(start), int(end)))

    allowed = allowed_ranges(blocked_ranges, MAX_IP)

    ##########
    # part 1 #
    ##########
    part_1 = allowed[0][0]
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = 0
    for first, last in allowed:
        part_2 += last - first + 1
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
