import os
from functools import lru_cache


@lru_cache(maxsize=None)
def stone_count(num, blinks):
    if blinks == 0:
        return 1
    elif num == 0:
        return stone_count(1, blinks - 1)
    elif len(str(num)) % 2 == 0:
        new_len = int(len(str(num)) / 2)
        return stone_count(int(str(num)[:new_len]), blinks - 1) + stone_count(
            int(str(num)[new_len:]), blinks - 1
        )
    else:
        return stone_count(num * 2024, blinks - 1)


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read().strip()
    stones = list(map(int, content.split()))

    # ##########
    # # part 1 #
    # ##########
    print(sum(stone_count(s, 25) for s in stones))

    # ##########
    # # part 2 #
    # ##########
    print(sum(stone_count(s, 75) for s in stones))


if __name__ == "__main__":
    main()
