import os
from collections import deque


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    data = {}
    for line in lines:
        device, raw_outputs = line.split(":", 1)
        data[device] = tuple(raw_outputs.split())

    ##########
    # part 1 #
    ##########
    paths = deque()
    paths.append(("you",))
    out_paths = set()
    while paths:
        path = paths.pop()
        for device in data[path[-1]]:
            if device == "out":
                out_paths.add((*path, device))
            else:
                paths.append((*path, device))
    print("part 1:", len(out_paths))

    ##########
    # part 2 #
    ##########
    count_cache = {}

    def count_paths(current="svr", has_dac=False, has_fft=False):
        if current == "out":
            return 1 if has_dac and has_fft else 0
        key = (current, has_dac, has_fft)
        if key in count_cache:
            return count_cache[key]
        count = 0
        for next_device in data.get(current, []):
            new_has_dac = has_dac or (next_device == "dac")
            new_has_fft = has_fft or (next_device == "fft")
            count += count_paths(next_device, new_has_dac, new_has_fft)
        count_cache[key] = count
        return count

    part_2 = count_paths()
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
