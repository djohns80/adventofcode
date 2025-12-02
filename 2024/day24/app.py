import os
import re
from collections import deque
from itertools import combinations


def get_binary(wires, wire):
    return "".join(
        dict(
            sorted(
                {
                    w: str(int(v)) for w, v in wires.items() if w.startswith(wire)
                }.items(),
                reverse=True,
            )
        ).values()
    )


def run_gates(wires, gates):
    gates_que = deque(gates)
    output = wires.copy()
    while gates_que:
        gate = gates_que.popleft()
        try:
            match gate[1]:
                case "AND":
                    output[gate[3]] = output[gate[0]] & output[gate[2]]
                case "OR":
                    output[gate[3]] = output[gate[0]] | output[gate[2]]
                case "XOR":
                    output[gate[3]] = output[gate[0]] ^ output[gate[2]]
        except KeyError:
            gates_que.append(gate)
    return output


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read().split("\n\n")
    wires = {
        w[0]: bool(int(w[1]))
        for line in content[0].splitlines()
        for w in re.findall(r"((?:x|y)\d+):\s(\d)", line)
    }
    gates = [
        re.findall(r"(\S{3})\s(AND|OR|XOR)\s(\S{3})\s->\s(\S{3})", line)[0]
        for line in content[1].splitlines()
    ]

    ##########
    # part 1 #
    ##########
    # part_1 = run_gates(wires, gates)
    # print(int(get_binary(part_1, "z"), 2))

    ##########
    # part 2 #
    ##########
    part_2 = run_gates(wires, gates)
    print(bin(int(get_binary(wires, "x"), 2) + int(get_binary(wires, "y"), 2))[2:])
    print(get_binary(part_2, "z"))

    print(part_2["z06"])
    print(part_2["nvf"], "OR", part_2["jvk"])



    # outputs = set(g[3] for g in gates)
    # print(len(list(combinations(outputs, 8))))


if __name__ == "__main__":
    main()
