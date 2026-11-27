import os

START_PROGRAM = 0


def parse_pipes(lines):
    """Return {program: [programs it can communicate with directly]}."""
    pipes = {}
    for line in lines:
        if not line.strip():
            continue
        program_part, connections_part = line.split(" <-> ")
        connections = []
        for connection in connections_part.split(", "):
            connections.append(int(connection))
        pipes[int(program_part)] = connections
    return pipes


def find_group(pipes, start):
    """Return the set of programs that can reach start through the pipes."""
    group = {start}
    to_visit = [start]
    while to_visit:
        program = to_visit.pop()
        for neighbour in pipes[program]:
            if neighbour not in group:
                group.add(neighbour)
                to_visit.append(neighbour)
    return group


def count_groups(pipes):
    """Return how many separate groups the programs form."""
    grouped = set()
    group_count = 0
    for program in pipes:
        if program not in grouped:
            grouped.update(find_group(pipes, program))
            group_count += 1
    return group_count


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    pipes = parse_pipes(lines)

    ##########
    # part 1 #
    ##########
    part_1 = len(find_group(pipes, START_PROGRAM))
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = count_groups(pipes)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
