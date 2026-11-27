import os


def last_word(line):
    # e.g. "    - Continue with state B." -> "B"
    return line.split()[-1].rstrip(".:")


def parse_blueprint(lines):
    start_state = last_word(lines[0])
    steps = int(lines[1].split()[-2])

    # rules[state][current_value] = (value_to_write, move, next_state)
    rules = {}
    state = None
    current_value = None
    for line in lines[2:]:
        line = line.strip()
        if line.startswith("In state"):
            state = last_word(line)
            rules[state] = {}
        elif line.startswith("If the current value is"):
            current_value = int(last_word(line))
        elif line.startswith("- Write the value"):
            value_to_write = int(last_word(line))
        elif line.startswith("- Move one slot to the"):
            if last_word(line) == "right":
                move = 1
            else:
                move = -1
        elif line.startswith("- Continue with state"):
            next_state = last_word(line)
            rules[state][current_value] = (value_to_write, move, next_state)
    return start_state, steps, rules


def run_machine(start_state, steps, rules):
    # the tape only remembers the positions holding a 1; everything else is 0
    ones = set()
    cursor = 0
    state = start_state
    for _ in range(steps):
        if cursor in ones:
            current_value = 1
        else:
            current_value = 0
        value_to_write, move, state = rules[state][current_value]
        if value_to_write == 1:
            ones.add(cursor)
        else:
            ones.discard(cursor)
        cursor += move
    return ones


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    start_state, steps, rules = parse_blueprint(lines)

    ##########
    # part 1 #
    ##########
    part_1 = len(run_machine(start_state, steps, rules))
    print("part 1:", part_1)


if __name__ == "__main__":
    main()
