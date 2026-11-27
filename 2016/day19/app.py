import os


def winning_elf(elf_count):
    # This is the Josephus problem with every second elf removed.
    # Write elf_count as 2**m + extra, where 2**m is the largest power of two
    # that fits. With a power of two elves, each lap removes exactly half and
    # elf 1 always starts the next lap, so elf 1 wins. Otherwise, after
    # `extra` steals, 2 * extra elves have taken a turn and 2**m elves remain,
    # with elf 2 * extra + 1 about to start - so that elf wins.
    largest_power = 1
    while largest_power * 2 <= elf_count:
        largest_power *= 2
    extra = elf_count - largest_power
    return 2 * extra + 1


def winning_elf_stealing_across(elf_count):
    # Stealing from the elf across the circle follows a pattern in powers of
    # three instead of two. Let 3**m be the largest power of three that fits:
    # - with exactly 3**m elves, the last elf (elf_count) wins;
    # - adding elves one at a time from there, the winner starts at elf 1 and
    #   moves up by one per extra elf, until there are 2 * 3**m elves;
    # - after that it moves up by two per extra elf, reaching elf_count again
    #   at the next power of three.
    # (Checked against a step-by-step simulation for small elf counts.)
    largest_power = 1
    while largest_power * 3 <= elf_count:
        largest_power *= 3
    if elf_count == largest_power:
        return elf_count
    if elf_count <= 2 * largest_power:
        return elf_count - largest_power
    return 2 * elf_count - 3 * largest_power


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    elf_count = int(content.strip())

    ##########
    # part 1 #
    ##########
    part_1 = winning_elf(elf_count)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = winning_elf_stealing_across(elf_count)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
