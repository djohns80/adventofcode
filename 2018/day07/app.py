import os

WORKER_COUNT = 5
BASE_STEP_SECONDS = 60


def step_seconds(step, base_seconds):
    """Return how long a step takes: the base time plus A=1, B=2, ..., Z=26."""
    return base_seconds + ord(step) - ord("A") + 1


def assemble(prerequisites, worker_count=1, base_seconds=0):
    """Work through the steps, starting available steps alphabetically.

    prerequisites maps every step to the set of steps that must be finished first.
    Returns (the order the steps are completed in, the total seconds taken).
    With a single worker the order is simply "always do the first available step
    alphabetically", which is what part 1 asks for.
    """
    done = set()
    order = []
    in_progress = {}  # step -> second at which it finishes
    seconds = 0
    while len(order) < len(prerequisites):
        # Give idle workers the available steps, in alphabetical order.
        available = []
        for step, required in prerequisites.items():
            if step not in done and step not in in_progress and required <= done:
                available.append(step)
        available.sort()
        for step in available:
            if len(in_progress) == worker_count:
                break
            in_progress[step] = seconds + step_seconds(step, base_seconds)

        # Jump straight to the moment the next step (or steps) finish.
        seconds = min(in_progress.values())
        finished = []
        for step, finish_time in in_progress.items():
            if finish_time == seconds:
                finished.append(step)
        finished.sort()
        for step in finished:
            del in_progress[step]
            done.add(step)
            order.append(step)
    return "".join(order), seconds


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    prerequisites = {}
    for line in lines:
        # "Step C must be finished before step A can begin."
        words = line.split()
        before = words[1]
        after = words[7]
        prerequisites.setdefault(before, set())
        prerequisites.setdefault(after, set())
        prerequisites[after].add(before)

    ##########
    # part 1 #
    ##########
    part_1, _ = assemble(prerequisites)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    _, part_2 = assemble(prerequisites, WORKER_COUNT, BASE_STEP_SECONDS)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
