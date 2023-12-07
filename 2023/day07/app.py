import os
import functools
from collections import Counter


def classify(hand):
    counts = list(Counter(hand).values())
    counts.sort(reverse=True)
    if counts[0] == 5:
        return 7  # "Five of a kind"
    elif counts[0] == 4:
        return 6  # "Four of a kind"
    elif counts[0] == 3 and counts[1] == 2:
        return 5  # "Full house"
    elif counts[0] == 3:
        return 4  # "Three of a kind"
    elif counts[0] == 2 and counts[1] == 2:
        return 3  # "Two pair"
    elif counts[0] == 2:
        return 2  # "One pair"
    else:
        return 1  # "High card"


def convert(c, part):
    if c == "T":
        return 10
    elif c == "J":
        return 1 if part == 2 else 11
    elif c == "Q":
        return 12
    elif c == "K":
        return 13
    elif c == "A":
        return 14
    else:
        return int(c)


def compare(hand1, hand2):
    cards1 = hand1[0]
    cards2 = hand2[0]
    if classify(cards1) > classify(cards2):
        return 1
    elif classify(cards1) < classify(cards2):
        return -1
    else:
        for i, c in enumerate(cards1):
            if convert(c, 1) > convert(cards2[i], 1):
                return 1
            elif convert(c, 1) < convert(cards2[i], 1):
                return -1
        return 0


def classify_2(hand):
    counts = Counter(hand)
    if "J" not in hand:
        counts = list(counts.values())
        counts.sort(reverse=True)
        if counts[0] == 5:
            return 7  # "Five of a kind"
        elif counts[0] == 4:
            return 6  # "Four of a kind"
        elif counts[0] == 3 and counts[1] == 2:
            return 5  # "Full house"
        elif counts[0] == 3:
            return 4  # "Three of a kind"
        elif counts[0] == 2 and counts[1] == 2:
            return 3  # "Two pair"
        elif counts[0] == 2:
            return 2  # "One pair"
        else:
            return 1  # "High car
    else:
        joker_count = counts.pop("J")
        counts = list(counts.values())
        counts.sort(reverse=True)
        if joker_count == 5:
            return 7  # "Five of a kind"
        elif joker_count == 4:
            return 7  # "Five of a kind"
        elif joker_count == 3:
            if counts[0] == 2:
                return 7  # "Five of a kind"
            else:
                return 6  # "Four of a kind"
        elif joker_count == 2:
            if counts[0] == 3:
                return 7  # "Five of a kind"
            elif counts[0] == 2:
                return 6  # "Four of a kind"
            else:
                return 4  # "Three of a kind"
        else:
            if counts[0] == 4:
                return 7  # "Five of a kind"
            elif counts[0] == 3:
                return 6  # "Four of a kind"
            elif counts[0] == 2 and counts[1] == 2:
                return 5  # "Full house"
            elif counts[0] == 2:
                return 4  # "Three of a kind"
            else:
                return 2  # "One pair"


def compare_2(hand1, hand2):
    cards1 = hand1[0]
    cards2 = hand2[0]
    if classify_2(cards1) > classify_2(cards2):
        return 1
    elif classify_2(cards1) < classify_2(cards2):
        return -1
    else:
        for i, c in enumerate(cards1):
            if convert(c, 2) > convert(cards2[i], 2):
                return 1
            elif convert(c, 2) < convert(cards2[i], 2):
                return -1
        return 0


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))
    hands = [([*line.split(" ")[0]], int(line.split(" ")[1])) for line in lines]

    ##########
    # part 1 #
    ##########
    ranks_1 = sorted(hands, key=functools.cmp_to_key(compare))
    print(sum([(r + 1) * h[1] for r, h in enumerate(ranks_1)]))

    ##########
    # part 2 #
    ##########
    ranks_2 = sorted(hands, key=functools.cmp_to_key(compare_2))
    print(sum([(r + 1) * h[1] for r, h in enumerate(ranks_2)]))


if __name__ == "__main__":
    main()
