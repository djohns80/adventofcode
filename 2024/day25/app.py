import os


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read().split("\n\n")
    locks = []
    keys = []
    for section in content:
        lines = section.splitlines()
        match lines[0]:
            case "#####":  # Lock
                locks.append(
                    tuple(sum(line[x] == "#" for line in lines[1:]) for x in range(5))
                )
            case ".....":  # Key
                keys.append(
                    tuple(sum(line[x] == "#" for line in lines[:-1]) for x in range(5))
                )

    ##########
    # part 1 #
    ##########
    print(
        sum(
            all((lock[n] + key[n]) <= 5 for n in range(5))
            for lock in locks
            for key in keys
        )
    )

    ##########
    # part 2 #
    ##########


if __name__ == "__main__":
    main()
