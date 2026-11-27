import os

DISK_LENGTH = 272
SECOND_DISK_LENGTH = 35651584

# swaps every 0 for a 1 and every 1 for a 0
FLIP_BITS = str.maketrans("01", "10")


def dragon_step(a):
    b = a[::-1].translate(FLIP_BITS)
    return a + "0" + b


def generate_data(initial_state, length):
    data = initial_state
    while len(data) < length:
        data = dragon_step(data)
    return data[:length]


def checksum(data):
    result = data
    while len(result) % 2 == 0:
        pairs = []
        for first, second in zip(result[0::2], result[1::2]):
            if first == second:
                pairs.append("1")
            else:
                pairs.append("0")
        result = "".join(pairs)
    return result


def disk_checksum(initial_state, length):
    return checksum(generate_data(initial_state, length))


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    initial_state = content.strip()

    ##########
    # part 1 #
    ##########
    part_1 = disk_checksum(initial_state, DISK_LENGTH)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = disk_checksum(initial_state, SECOND_DISK_LENGTH)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
