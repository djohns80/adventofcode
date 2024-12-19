import os
import re
from functools import lru_cache


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read().split("\n\n")
    towels = set(re.findall(r"\w+", content[0]))
    designs = content[1].splitlines()

    @lru_cache(maxsize=None)
    def count_patterns(design):
        if design == "":
            return 1
        starter_patterns = [p for p in towels if design.startswith(p)]
        if len(starter_patterns) == 0:
            return 0
        return sum(
            count_patterns(design[len(pattern) :]) for pattern in starter_patterns
        )

    ##########
    # part 1 #
    ##########
    print(sum(count_patterns(design) != 0 for design in designs))

    ##########
    # part 2 #
    ##########
    print(sum(count_patterns(design) for design in designs))


if __name__ == "__main__":
    main()
