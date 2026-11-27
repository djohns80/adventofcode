import os


def parse_layers(lines):
    layers = {}
    for line in lines:
        depth, scan_range = line.split(":")
        layers[int(depth)] = int(scan_range)
    return layers


def scanner_at_top(scan_range, time):
    # a scanner goes down and back up again, so it is at the top every
    # 2 * (range - 1) picoseconds
    if scan_range == 1:
        return True
    return time % (2 * (scan_range - 1)) == 0


def caught_layers(layers, delay=0, stop_at_first=False):
    # the packet enters the layer at depth d at picosecond delay + d
    caught = []
    for depth, scan_range in layers.items():
        if scanner_at_top(scan_range, delay + depth):
            caught.append(depth)
            if stop_at_first:
                break
    return caught


def trip_severity(layers, delay=0):
    severity = 0
    for depth in caught_layers(layers, delay):
        severity += depth * layers[depth]
    return severity


def fewest_safe_delay(layers):
    # severity can't be used here: being caught at depth 0 has severity 0
    delay = 0
    while caught_layers(layers, delay, stop_at_first=True):
        delay += 1
    return delay


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    layers = parse_layers(lines)

    ##########
    # part 1 #
    ##########
    part_1 = trip_severity(layers)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = fewest_safe_delay(layers)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
