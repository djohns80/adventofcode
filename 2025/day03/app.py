import os


def get_largest_joltage(bank, battery_count=2):
    stack = []
    to_remove = len(bank) - battery_count
    for digit in bank:
        while stack and stack[-1] < digit and to_remove > 0:
            stack.pop()
            to_remove -= 1
        stack.append(digit)
    return int("".join(str(v) for v in stack[:battery_count]))


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = [line.strip() for line in content.splitlines()]
    banks = [[int(v) for v in line] for line in lines]

    ##########
    # part 1 #
    ##########
    print("part 1:", sum(get_largest_joltage(bank) for bank in banks))

    ##########
    # part 2 #
    ##########
    print("part 2:", sum(get_largest_joltage(bank, 12) for bank in banks))


if __name__ == "__main__":
    main()
