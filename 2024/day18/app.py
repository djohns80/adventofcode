import os
from collections import deque

moves = (1, -1, 1j, -1j)


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = content.splitlines()
    incoming_bytes = [complex(*list(map(int, line.split(",")))) for line in lines]
    # dim = [6, 6]
    dim = [70, 70]

    ##########
    # part 1 #
    ##########
    fallen_bytes = set(incoming_bytes[:1024])
    steps = {}
    queue = deque([(complex(0, 0), 0)])
    while queue:
        pos, cur_steps = queue.popleft()
        for move in moves:
            new_pos = pos + move
            if new_pos in fallen_bytes:
                continue
            if new_pos.real in range(dim[0] + 1) and new_pos.imag in range(dim[1] + 1):
                if (new_pos not in steps) or (
                    new_pos in steps and steps[new_pos] > cur_steps + 1
                ):
                    queue.append((new_pos, cur_steps + 1))
                    steps[new_pos] = cur_steps + 1
    print(steps[complex(*dim)])

    ##########
    # part 2 #
    ##########
    lower = 0
    upper = len(incoming_bytes) - 1
    while upper - lower > 1:
        test = int((upper - lower) / 2) + lower
        fallen_bytes = incoming_bytes[:test]
        steps = {}
        queue = deque([(complex(0, 0), 0)])
        while queue:
            pos, cur_steps = queue.popleft()
            for move in moves:
                new_pos = pos + move
                if new_pos in fallen_bytes:
                    continue
                if new_pos.real in range(dim[0] + 1) and new_pos.imag in range(
                    dim[1] + 1
                ):
                    if (new_pos not in steps) or (
                        new_pos in steps and steps[new_pos] > cur_steps + 1
                    ):
                        queue.append((new_pos, cur_steps + 1))
                        steps[new_pos] = cur_steps + 1
        if complex(*dim) not in steps:
            upper = test
        else:
            lower = test
    print(
        ",".join(
            [str(int(incoming_bytes[lower].real)), str(int(incoming_bytes[lower].imag))]
        )
    )


if __name__ == "__main__":
    main()
