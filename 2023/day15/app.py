import os
import re
import math
from collections import defaultdict


def hash_algorithm(string):
    current_value = 0
    for c in list(string):
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


def parse(value):
    match = re.match(r"(?P<label>\w+)(?P<operation>[=-])(?P<focal_length>\d+)?", value)
    if match:
        return match.groupdict()
    return None


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    sequence = file.read().strip().split(",")

    ##########
    # part 1 #
    ##########
    print(sum(hash_algorithm(s) for s in sequence))

    ##########
    # part 2 #
    ##########
    boxes = defaultdict(list)
    for seq in sequence:
        s = parse(seq)
        if s["operation"] == "-":
            boxes[hash_algorithm(s["label"])] = [
                lense
                for lense in boxes[hash_algorithm(s["label"])]
                if not lense[0] == s["label"]
            ]
        elif s["operation"] == "=":
            existing_index = [
                boxes[hash_algorithm(s["label"])].index(lense)
                for lense in boxes[hash_algorithm(s["label"])]
                if lense[0] == s["label"]
            ]
            if existing_index:
                boxes[hash_algorithm(s["label"])][existing_index[0]] = (
                    s["label"],
                    int(s["focal_length"]),
                )
            else:
                boxes[hash_algorithm(s["label"])].append(
                    (s["label"], int(s["focal_length"]))
                )
    part_2 = 0
    for k, v in boxes.items():
        for s, lense in enumerate(v):
            part_2 += math.prod([k + 1, s + 1, lense[1]])
    print(part_2)


if __name__ == "__main__":
    main()
