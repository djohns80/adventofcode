import os


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    secret_numbers = list(map(int, content.splitlines()))

    part_1 = 0
    part_2 = {}
    for secret_number in secret_numbers:
        seen = set()
        last_4 = (10, 10, 10, 10)
        for _ in range(2000):
            prev = secret_number % 10
            secret_number ^= secret_number * 64 % 16777216
            secret_number ^= secret_number // 32 % 16777216
            secret_number ^= secret_number * 2048 % 16777216
            last_4 = last_4[1:] + (secret_number % 10 - prev,)
            if last_4 not in seen:
                seen.add(last_4)
                part_2[last_4] = part_2.get(last_4, 0) + secret_number % 10
        part_1 += secret_number

    ##########
    # part 1 #
    ##########
    print(part_1)

    ##########
    # part 2 #
    ##########
    print(max(part_2.values()))


if __name__ == "__main__":
    main()
