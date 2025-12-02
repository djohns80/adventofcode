import os


def is_repeated_pattern(num_str, num_len):
    for sub_len in range(1, (num_len // 2) + 1):
        if num_len % sub_len == 0 and num_str == num_str[:sub_len] * (
            num_len // sub_len
        ):
            # Early return once repeat found
            return True
    return False


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = [line.strip() for line in content.split(",")]
    ranges = [[int(v) for v in line.split("-")] for line in lines]

    part_1 = 0
    part_2 = 0
    for start, end in ranges:
        for num in range(start, end + 1):
            num_str = str(num)
            num_len = len(num_str)
            # Early return for single digit ids
            if num_len == 1:
                continue

            if num_len % 2 == 0:
                if num_str[: num_len // 2] == num_str[num_len // 2 :]:
                    part_1 += num

            if is_repeated_pattern(num_str, num_len):
                part_2 += num

    ##########
    # part 1 #
    ##########
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
