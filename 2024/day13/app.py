import os
import re


def win_tokens(m, conversion=0):
    A = int(
        (
            (m["P"].real + conversion) * m["B"].imag
            - (m["P"].imag + conversion) * m["B"].real
        )
        / (m["B"].imag * m["A"].real - m["B"].real * m["A"].imag)
    )
    B = int(
        (
            (m["P"].real + conversion) * m["A"].imag
            - (m["P"].imag + conversion) * m["A"].real
        )
        / (m["A"].imag * m["B"].real - m["B"].imag * m["A"].real)
    )
    if m["A"] * A + m["B"] * B == (m["P"] + (conversion + conversion * 1j)):
        return 3 * A + B
    else:
        return 0


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    values = re.findall(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
        content,
    )
    machines = [
        {
            "A": int(v[0]) + int(v[1]) * 1j,
            "B": int(v[2]) + int(v[3]) * 1j,
            "P": int(v[4]) + int(v[5]) * 1j,
        }
        for v in values
    ]

    ##########
    # part 1 #
    ##########
    print(sum([win_tokens(machine) for machine in machines]))

    ##########
    # part 2 #
    ##########
    print(sum([win_tokens(machine, 10000000000000) for machine in machines]))


if __name__ == "__main__":
    main()
