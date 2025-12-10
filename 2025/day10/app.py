import os
import re
from scipy.optimize import milp, LinearConstraint, Bounds


def solve_indicator(indicator, buttons):
    min_presses = float("inf")
    # Loop all button press combinations
    for combo in range(2 ** len(buttons)):
        lights = [0] * len(indicator)
        presses = 0
        for i, button in enumerate(buttons):
            # Does this combination include this button?
            if combo & (1 << i):
                presses += 1
                for light in button:
                    lights[light] ^= 1
        if lights == indicator:
            min_presses = min(min_presses, presses)
    return min_presses


def solve_joltage(joltage, buttons):
    # Which button affects which counter
    coefficient_matrix = [[0] * len(buttons) for _ in range(len(joltage))]
    for i, button in enumerate(buttons):
        for counter in button:
            coefficient_matrix[counter][i] = 1

    # Solve and return result
    result = milp(
        [1]
        * len(buttons),  # Minimise presses, and all button presses have equal weighting
        constraints=LinearConstraint(coefficient_matrix, joltage, joltage),
        bounds=Bounds(0, float("inf")),  # Negative button presses not allowed
        integrality=[1]
        * len(buttons),  # Solution must use integers, partial presses not allowed
    )
    return int(sum(result.x))


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    machines = []
    for line in lines:
        match = re.match(
            r"\[(?P<indicator>[^\]]+)\]\s+(?P<buttons>(?:\([^)]+\)\s*)+)\s*\{(?P<joltage>[^}]+)\}",
            line,
        )
        machines.append(
            {
                "indicator": [int(i == "#") for i in match.group("indicator")],
                "buttons": tuple(
                    tuple(map(int, button.split(",")))
                    for button in re.findall(r"\(([^)]+)\)", match.group("buttons"))
                ),
                "joltage": tuple(int(j) for j in match.group("joltage").split(",")),
            }
        )

    ##########
    # part 1 #
    ##########
    part_1 = sum(
        solve_indicator(machine["indicator"], machine["buttons"])
        for machine in machines
    )
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = sum(
        solve_joltage(machine["joltage"], machine["buttons"]) for machine in machines
    )
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
