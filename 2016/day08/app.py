import os

SCREEN_WIDTH = 50
SCREEN_HEIGHT = 6


def parse_instruction(line):
    # returns ("rect", width, height), ("row", y, amount) or ("column", x, amount)
    words = line.split()
    if words[0] == "rect":
        width, height = words[1].split("x")
        return ("rect", int(width), int(height))
    # e.g. "rotate row y=0 by 4" or "rotate column x=1 by 1"
    index = int(words[2].split("=")[1])
    amount = int(words[4])
    return (words[1], index, amount)


def apply_instruction(screen, instruction):
    height = len(screen)
    width = len(screen[0])
    if instruction[0] == "rect":
        _, rect_width, rect_height = instruction
        for y in range(rect_height):
            for x in range(rect_width):
                screen[y][x] = True
    elif instruction[0] == "row":
        _, y, amount = instruction
        old_row = screen[y]
        # shift right: the new pixel at x came from x - amount
        new_row = []
        for x in range(width):
            new_row.append(old_row[(x - amount) % width])
        screen[y] = new_row
    elif instruction[0] == "column":
        _, x, amount = instruction
        old_column = []
        for y in range(height):
            old_column.append(screen[y][x])
        # shift down: the new pixel at y came from y - amount
        for y in range(height):
            screen[y][x] = old_column[(y - amount) % height]


def run_screen(instructions, width, height):
    screen = []
    for _ in range(height):
        screen.append([False] * width)
    for instruction in instructions:
        apply_instruction(screen, instruction)
    return screen


def count_lit(screen):
    total = 0
    for row in screen:
        for pixel in row:
            if pixel:
                total += 1
    return total


def render(screen):
    # returns one string per row, "#" for on and "." for off
    rows = []
    for row in screen:
        text = ""
        for pixel in row:
            if pixel:
                text += "#"
            else:
                text += "."
        rows.append(text)
    return rows


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    instructions = []
    for line in lines:
        instructions.append(parse_instruction(line))

    ##########
    # part 1 #
    ##########
    screen = run_screen(instructions, SCREEN_WIDTH, SCREEN_HEIGHT)
    part_1 = count_lit(screen)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    # the screen shows letters, so draw it and read them by eye
    print("part 2:")
    for row in render(screen):
        print(row)


if __name__ == "__main__":
    main()
