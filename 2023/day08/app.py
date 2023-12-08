import os
import re
import math


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = list(map(str.strip, file.readlines()))
    instructions = [*lines.pop(0)]
    nodes = {
        raw[0]: {"L": raw[1], "R": raw[2]}
        for raw in [re.findall(r"[A-Z0-9]+", line) for line in lines if line != ""]
    }

    ##########
    # part 1 #
    ##########
    current_node = "AAA"
    steps = 0
    while current_node != "ZZZ":
        instruction = instructions[steps % len(instructions)]
        current_node = nodes[current_node][instruction]
        steps += 1
    print(steps)

    ##########
    # part 2 #
    ##########
    current_nodes = [node for node in nodes.keys() if node.endswith("A")]

    # ###################################################################################
    # # Code to check/prove that the paths all loop so that LCM can be used to shortcut #
    # ###################################################################################
    # for current_node in current_nodes:
    #     steps = 0
    #     first_loop = 0
    #     while steps < 100000:
    #         instruction = instructions[steps % len(instructions)]
    #         current_node = nodes[current_node][instruction]
    #         steps += 1
    #         if current_node.endswith("A") or current_node.endswith("Z"):
    #             if first_loop == 0:
    #                 first_loop = steps
    #             print(current_node, steps, first_loop, steps / first_loop)
    # ###################################################################################

    all_steps = []
    for current_node in current_nodes:
        steps = 0
        while not current_node.endswith("Z"):
            instruction = instructions[steps % len(instructions)]
            current_node = nodes[current_node][instruction]
            steps += 1
        all_steps.append(steps)
    print(math.lcm(*all_steps))


if __name__ == "__main__":
    main()
