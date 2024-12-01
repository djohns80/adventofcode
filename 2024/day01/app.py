import os


def main():
    ##########
    # part 1 #
    ##########
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = [line.strip() for line in content.splitlines()]
    lists = list(zip(*[map(int, line.split()) for line in lines]))
    print(
        sum(abs(pair[0] - pair[1]) for pair in zip(sorted(lists[0]), sorted(lists[1])))
    )

    ##########
    # part 2 #
    ##########
    print(
        sum(
            [
                v * (len(lists[1]) - len(list(filter(lambda k: k != v, lists[1]))))
                for v in lists[0]
            ]
        )
    )


if __name__ == "__main__":
    main()
