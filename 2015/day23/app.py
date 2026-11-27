import os


def run_program(a_value, program):
    registers = {"a": a_value, "b": 0}
    i = 0
    while 0 <= i < len(program):
        instr, reg, offset = program[i]
        match instr:
            case "hlf":
                registers[reg] //= 2
            case "tpl":
                registers[reg] *= 3
            case "inc":
                registers[reg] += 1
            case "jmp":
                i += offset
                continue
            case "jie":
                if registers[reg] % 2 == 0:
                    i += offset
                    continue
            case "jio":
                if registers[reg] == 1:
                    i += offset
                    continue
        i += 1
    return registers["b"]


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    program = []
    for line in lines:
        instr, *args = line.replace(",", " ").split()
        reg = args.pop(0) if args[0] in ("a", "b") else None
        offset = int(args[0]) if args else None
        program.append((instr, reg, offset))

    ##########
    # part 1 #
    ##########
    print("part 1:", run_program(0, program))

    ##########
    # part 2 #
    ##########
    print("part 2:", run_program(1, program))


if __name__ == "__main__":
    main()
