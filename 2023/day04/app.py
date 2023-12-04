import os
import re


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = [line.strip() for line in file.readlines()]
    cards = []
    for line in lines:
        parsed = list(
            re.findall(r"^Card\s+(\d+):\s+((?:\d+\s+)+)\|((?:\s+\d+)+)$", line)
        )
        cards.append(
            [
                int(parsed[0][0]),
                [int(v) for v in parsed[0][1].split()],
                [int(v) for v in parsed[0][2].split()],
                1,
            ]
        )

    ##########
    # part 1 #
    ##########
    part_1 = 0
    for card in cards:
        match_count = len(set(card[1]).intersection(set(card[2])))
        if match_count > 0:
            part_1 += 2 ** (match_count - 1)
    print(part_1)

    ##########
    # part 2 #
    ##########
    for i, card in enumerate(cards):
        match_count = len(set(card[1]).intersection(set(card[2])))
        for n in list(range(i + 1, i + 1 + match_count)):
            cards[n][3] += card[3]
    print(sum([c[3] for c in cards]))


if __name__ == "__main__":
    main()
