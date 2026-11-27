import os

RAW_MATERIAL = "ORE"
PRODUCT = "FUEL"
ORE_AVAILABLE = 1_000_000_000_000


def parse_reactions(lines):
    """Return {output chemical: (output quantity, [(input quantity, input chemical)])}."""
    reactions = {}
    for line in lines:
        raw_inputs, raw_output = line.split(" => ")
        output_quantity, output_chemical = raw_output.split()
        inputs = []
        for raw_input in raw_inputs.split(", "):
            input_quantity, input_chemical = raw_input.split()
            inputs.append((int(input_quantity), input_chemical))
        reactions[output_chemical] = (int(output_quantity), inputs)
    return reactions


def ore_required(reactions, fuel_amount=1):
    """Return the ORE needed to make fuel_amount FUEL, reusing leftover chemicals."""
    to_make = [(PRODUCT, fuel_amount)]
    leftovers = {}
    ore = 0
    while to_make:
        chemical, amount = to_make.pop()
        if chemical == RAW_MATERIAL:
            ore += amount
            continue

        # use up any spare units left over from earlier reactions first
        spare = leftovers.get(chemical, 0)
        used_spare = min(spare, amount)
        leftovers[chemical] = spare - used_spare
        amount -= used_spare
        if amount == 0:
            continue

        output_quantity, inputs = reactions[chemical]
        runs = (amount + output_quantity - 1) // output_quantity  # round up
        leftovers[chemical] += runs * output_quantity - amount
        for input_quantity, input_chemical in inputs:
            to_make.append((input_chemical, input_quantity * runs))
    return ore


def most_fuel(reactions, ore_available):
    """Return the most FUEL that can be made from ore_available ORE."""
    # making fuel in bulk wastes less, so the cost of 1 FUEL gives a lower bound
    low = ore_available // ore_required(reactions)
    high = low + 1
    while ore_required(reactions, high) <= ore_available:
        high *= 2

    # binary search, keeping low affordable and high too expensive
    while high - low > 1:
        middle = (low + high) // 2
        if ore_required(reactions, middle) <= ore_available:
            low = middle
        else:
            high = middle
    return low


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    reactions = parse_reactions(lines)

    ##########
    # part 1 #
    ##########
    part_1 = ore_required(reactions)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = most_fuel(reactions, ORE_AVAILABLE)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
