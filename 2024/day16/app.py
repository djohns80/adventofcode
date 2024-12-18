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

    start = 1 + ((len(lines) - 2) * 1j)
    end = (len(lines) - 2) + 1j
    walls = set(
        x + y * 1j for y, row in enumerate(lines) for x, c in enumerate(row) if c == "#"
    )

    ##########
    # part 1 #
    ##########
    scores = {1: {start: 0}, -1: {}, 1j: {}, -1j: {}}
    points = deque([(start, 1)])
    while points:
        pos, fac = points.popleft()
        score = scores[fac][pos]
        for new_pos, new_fac, cost in [
            (pos + fac, fac, 1),
            (pos, fac * -1j, 1000),
            (pos, fac * 1j, 1000),
        ]:
            if new_pos not in walls and (
                new_pos not in scores[new_fac]
                or scores[new_fac][new_pos] > score + cost
            ):
                scores[new_fac][new_pos] = score + cost
                points.append((new_pos, new_fac))

    min_score = min(scores[d][end] for d in moves if end in scores[d])
    print(min_score)

    ##########
    # part 2 #
    ##########
    path = {start, end}
    points = deque(
        [
            (end, d, min_score)
            for d in moves
            if end in scores[d] and scores[d][end] == min_score
        ]
    )
    while points:
        pos, fac, min_score = points.popleft()
        for new_pos, new_fac, cost in [
            (pos - fac, fac, min_score - 1),
            (pos, fac * 1j, min_score - 1000),
            (pos, fac * -1j, min_score - 1000),
        ]:
            if new_pos in scores[new_fac] and scores[new_fac][new_pos] == cost:
                path.add(new_pos)
                points.append((new_pos, new_fac, cost))
    print(len(path))


if __name__ == "__main__":
    main()
