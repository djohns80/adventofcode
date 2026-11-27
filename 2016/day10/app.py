import os

LOW_CHIP_TO_FIND = 17
HIGH_CHIP_TO_FIND = 61
OUTPUT_BINS_TO_MULTIPLY = (0, 1, 2)


def parse_instructions(lines):
    # starting_chips: list of (value, bot number)
    # rules: bot number -> ((low kind, low number), (high kind, high number))
    # where kind is "bot" or "output"
    starting_chips = []
    rules = {}
    for line in lines:
        words = line.split()
        if words[0] == "value":
            # value 5 goes to bot 2
            starting_chips.append((int(words[1]), int(words[5])))
        else:
            # bot 2 gives low to bot 1 and high to bot 0
            bot = int(words[1])
            low_target = (words[5], int(words[6]))
            high_target = (words[10], int(words[11]))
            rules[bot] = (low_target, high_target)
    return starting_chips, rules


def run_factory(starting_chips, rules):
    # returns (comparisons, outputs) where comparisons maps
    # (low chip, high chip) -> bot number that compared them
    bots = {}
    outputs = {}
    comparisons = {}
    for value, bot in starting_chips:
        bots.setdefault(bot, []).append(value)

    # bots holding two chips are ready to hand them on
    ready = []
    for bot, chips in bots.items():
        if len(chips) == 2:
            ready.append(bot)

    while ready:
        bot = ready.pop()
        low_chip = min(bots[bot])
        high_chip = max(bots[bot])
        bots[bot] = []
        comparisons[(low_chip, high_chip)] = bot
        low_target, high_target = rules[bot]
        for chip, (kind, number) in ((low_chip, low_target), (high_chip, high_target)):
            if kind == "output":
                outputs.setdefault(number, []).append(chip)
            else:
                bots.setdefault(number, []).append(chip)
                if len(bots[number]) == 2:
                    ready.append(number)
    return comparisons, outputs


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    starting_chips, rules = parse_instructions(lines)

    ##########
    # part 1 #
    ##########
    comparisons, outputs = run_factory(starting_chips, rules)
    part_1 = comparisons[(LOW_CHIP_TO_FIND, HIGH_CHIP_TO_FIND)]
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # each of these output bins ends up holding exactly one chip
    part_2 = 1
    for output_bin in OUTPUT_BINS_TO_MULTIPLY:
        part_2 *= outputs[output_bin][0]
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
