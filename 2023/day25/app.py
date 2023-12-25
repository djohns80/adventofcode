import os


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))

    print(lines)

    ##########
    # part 1 #
    ##########


    ##########
    # part 2 #
    ##########


if __name__ == "__main__":
    main()
