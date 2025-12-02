import os


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = [line.strip() for line in content.splitlines()]
    rotations = [(line[0], int(line[1:])) for line in lines]

    dial_value = 50
    zero_pass = 0
    zero_land = 0

    for direction, amount in rotations:
        # Count full rotations (each crosses zero once)
        zero_pass += amount // 100
        remainder = amount % 100

        # Calculate new position
        unbouded_dial_value = dial_value + (
            remainder if direction == "R" else -remainder
        )
        new_dial_value = unbouded_dial_value % 100

        # Count if we landed on zero
        if new_dial_value == 0:
            zero_land += 1
        # Count if we crossed zero (without landing on it)
        elif dial_value != 0 and unbouded_dial_value != new_dial_value:
            zero_pass += 1

        dial_value = new_dial_value

    ##########
    # part 1 #
    ##########
    print("part 1:", zero_land)

    ##########
    # part 2 #
    ##########
    print("part 2:", zero_pass + zero_land)


if __name__ == "__main__":
    main()
