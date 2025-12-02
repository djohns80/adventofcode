import os


numerical_keypad = {
    "7": complex(0, 0),
    "8": complex(1, 0),
    "9": complex(2, 0),
    "4": complex(0, 1),
    "5": complex(1, 1),
    "6": complex(2, 1),
    "1": complex(0, 2),
    "2": complex(1, 2),
    "3": complex(2, 2),
    "X": complex(0, 3),
    "0": complex(1, 3),
    "A": complex(2, 3),
}

directional_keypad = {
    "X": complex(0, 0),
    "^": complex(1, 0),
    "A": complex(2, 0),
    "<": complex(0, 1),
    "v": complex(1, 1),
    ">": complex(2, 1),
}


def get_presses(pos_1, pos_2, avoid):
    diff_x = int(pos_2.real - pos_1.real)
    diff_y = int(pos_2.imag - pos_1.imag)
    button_x = ">" if diff_x > 0 else "<"
    button_y = "v" if diff_y > 0 else "^"
    if diff_x == 0:
        return [button_y] * abs(diff_y) + ["A"]
    if diff_y == 0:
        return [button_x] * abs(diff_x) + ["A"]
    if (pos_1 + complex(diff_x, 0)) == avoid:
        return [button_y] * abs(diff_y) + [button_x] * abs(diff_x) + ["A"]
    if (pos_1 + complex(0, diff_y)) == avoid:
        return [button_x] * abs(diff_x) + [button_y] * abs(diff_y) + ["A"]
    else:
        return (
            [button_y] * abs(diff_y) + [button_x] * abs(diff_x) + ["A"],
            [button_x] * abs(diff_x) + [button_y] * abs(diff_y) + ["A"],
        )


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    codes = content.splitlines()

    value = 0
    for code in codes[:1]:
    # code = codes[2]
        pos = numerical_keypad["A"]
        buttons_1 = []
        for button in code:
            new_pos = numerical_keypad[button]
            buttons_1.append(get_presses(pos, new_pos, numerical_keypad["X"]))
            pos = new_pos
        print(buttons_1)

    #     pos = directional_keypad["A"]
    #     buttons_2 = []
    #     for button in buttons_1:
    #         new_pos = directional_keypad[button]
    #         buttons_2.extend(get_presses(pos, new_pos))
    #         pos = new_pos
    #     print(len(buttons_2), "".join(buttons_2))

    #     pos = directional_keypad["A"]
    #     buttons_3 = []
    #     for button in buttons_2:
    #         new_pos = directional_keypad[button]
    #         buttons_3.extend(get_presses(pos, new_pos))
    #         pos = new_pos
    #     print(len(buttons_3), "".join(buttons_3))

    #     complexity = [len(buttons_3), int(code[:-1])]
    #     print(complexity)
    #     value += (complexity[0] * complexity[1])

    # print(value)

    ##########
    # part 1 #
    ##########

    ##########
    # part 2 #
    ##########


if __name__ == "__main__":
    main()
