import os
from collections import defaultdict, deque


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read().strip()
    height_groups = defaultdict(list)
    for y, line in enumerate(content.strip().splitlines()):
        for x, char in enumerate(line):
            height_groups[int(char)].append(x + y * 1j)

    complete_trailheads = []
    trailhead_queue = deque([[h] for h in height_groups[0]])
    while trailhead_queue:
        path = trailhead_queue.pop()
        if len(path) == 10:
            complete_trailheads.append(path)
        for next_step in height_groups[len(path)]:
            if abs(path[-1] - next_step) == 1:
                trailhead_queue.append([*path, next_step])

    ##########
    # part 1 #
    ##########
    print(len(set((th[0], th[-1]) for th in complete_trailheads)))

    ##########
    # part 2 #
    ##########
    print(len(complete_trailheads))


if __name__ == "__main__":
    main()
