import os


def process_stream(stream):
    """Return the total score of all groups and the number of garbage characters.

    Garbage characters exclude the enclosing < and >, the ! marks and whatever
    each ! cancels.
    """
    total_score = 0
    garbage_count = 0
    depth = 0
    in_garbage = False
    skip_next = False
    for character in stream:
        if skip_next:
            skip_next = False
        elif in_garbage:
            if character == "!":
                skip_next = True
            elif character == ">":
                in_garbage = False
            else:
                garbage_count += 1
        elif character == "<":
            in_garbage = True
        elif character == "{":
            depth += 1
            total_score += depth
        elif character == "}":
            depth -= 1
    return total_score, garbage_count


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    stream = content.strip()
    total_score, garbage_count = process_stream(stream)

    ##########
    # part 1 #
    ##########
    part_1 = total_score
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = garbage_count
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
