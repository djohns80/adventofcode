import os


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = [line.strip() for line in file.readlines() if line.strip() != ""]
    seeds = list(map(int, lines.pop(0).split(" ")[1:]))
    maps = {}
    for line in lines:
        if ":" in line:
            type_split = line[0:-5].split("-to-")
            type_id = type_split[0]
            maps[type_id] = {}
        else:
            ranges = list(map(int, line.split(" ")))
            maps[type_id][range(ranges[1], ranges[1] + ranges[2])] = ranges[0]

    ##########
    # part 1 #
    ##########
    lowest_location = None
    for seed in seeds:
        location = seed
        for resource_range in maps.values():
            for source_range, base in resource_range.items():
                if location in source_range:
                    location = base + location - source_range[0]
                    break
        if lowest_location is None or location < lowest_location:
            lowest_location = location
    print(lowest_location)

    ##########
    # part 2 #
    ##########
    seed_ranges = [
        range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)
    ]
    location_ranges = seed_ranges
    for range_map in maps.values():
        destination_ranges = []
        remaining = location_ranges
        for d_range, base in range_map.items():
            next_set = []
            for s_range in remaining:
                # source_range is outside of destination_range
                if s_range[-1] < d_range[0] or d_range[-1] < s_range[0]:
                    next_set.append(s_range)
                # source_range contains destination_range
                if s_range[0] < d_range[0] and d_range[-1] < s_range[-1]:
                    # add overlap
                    destination_ranges.append(range(base, base + len(d_range)))
                    # add lower outside range
                    next_set.append(range(s_range[0], d_range[0]))
                    # add upper outside range
                    next_set.append(range(d_range[-1] + 1, s_range[-1] + 1))
                # destination_range contains source_range
                if d_range[0] <= s_range[0] and s_range[-1] <= d_range[-1]:
                    start = s_range[0] - d_range[0] + base 
                    # add overlap
                    destination_ranges.append(range(start, start + len(s_range)))
                # source_range overlaps at lower end
                if s_range[0] < d_range[0] <= s_range[-1] <= d_range[-1]:
                    start = base
                    end = base + s_range[-1] - d_range[0] + 1
                    # add overlap
                    destination_ranges.append(range(start, end))
                    # add lower outside range
                    next_set.append(range(s_range[0], d_range[0]))
                # source_range overlaps at upper end
                if d_range[0] <= s_range[0] <= d_range[-1] < s_range[-1]:
                    start = base + s_range[0] - d_range[0]
                    end = base + len(d_range)
                    # add overlap
                    destination_ranges.append(range(start, end))
                    # add upper outside range
                    next_set.append(range(d_range[-1] + 1, s_range[-1] + 1))
            remaining = next_set
        destination_ranges.extend(remaining)
        location_ranges = destination_ranges
    print(min(r[0] for r in location_ranges))


if __name__ == "__main__":
    main()
