import os


def update_valid(update, rules):
    return all(
        all(
            (
                (n < update.index(rule[1]))
                if page == rule[0]
                else (update.index(rule[0]) < n)
            )
            for rule in [r for r in rules if page in r]
        )
        for n, page in enumerate(update)
    )


def rule_valid(rule, update):
    indexes = (update.index(rule[0]), update.index(rule[1]))
    return indexes[0] < indexes[1], indexes


def swap_positions(update, positions):
    temp = update[positions[0]]
    update[positions[0]] = update[positions[1]]
    update[positions[1]] = temp


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    lines = [line.strip() for line in content.splitlines()]
    rules = [list(map(int, line.split("|"))) for line in lines if "|" in line]
    updates = [list(map(int, line.split(","))) for line in lines if "," in line]

    ##########
    # part 1 #
    ##########
    valid_updates = []
    invalid_updates = []
    for update in updates:
        applicable_rules = [r for r in rules if r[0] in update and r[1] in update]
        valid_update = update_valid(update, applicable_rules)
        if valid_update:
            valid_updates.append((update, applicable_rules))
        else:
            invalid_updates.append((update, applicable_rules))
    middle_pages = [update[int(len(update) / 2)] for update, _ in valid_updates]
    print(sum(middle_pages))

    ##########
    # part 2 #
    ##########
    for update, rules in invalid_updates:
        for rule in rules:
            valid_rule, indexes = rule_valid(rule, update)
            if not valid_rule:
                swap_positions(update, indexes)
        while not update_valid(update, rules):
            for rule in rules:
                valid_rule, indexes = rule_valid(rule, update)
                if not valid_rule:
                    swap_positions(update, indexes)
    middle_pages = [update[int(len(update) / 2)] for update, _ in invalid_updates]
    print(sum(middle_pages))


if __name__ == "__main__":
    main()
