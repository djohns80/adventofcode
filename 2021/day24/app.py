import z3

if __name__ == '__main__':
#    file = open('sample', 'r', encoding='utf-8')
    file = open('input', 'r', encoding='utf-8')
    lines = [l.strip().split(' ') for l in file.readlines()]

    solver = z3.Optimize()
    digits = [z3.BitVec(f'd_{i}', 64) for i in range(14)]
    for d in digits:
        solver.add(1 <= d)
        solver.add(d <= 9)
    digit_input = iter(digits)
    zero, one = z3.BitVecVal(0, 64), z3.BitVecVal(1, 64)
    registers = {v: zero for v in 'xyzw'}
    for i, inst in enumerate(lines):
        if inst[0] == 'inp':
            registers[inst[1]] = next(digit_input)
            continue
        a, b = inst[1:]
        b = registers[b] if b in registers else int(b)
        c = z3.BitVec(f'v_{i}', 64)
        match inst[0]:
            case 'add':
                solver.add(c == registers[a] + b)
            case 'mul':
                solver.add(c == registers[a] * b)
            case 'mod':
                solver.add(registers[a] >= 0)
                solver.add(b > 0)
                solver.add(c == registers[a] % b)
            case 'div':
                solver.add(b != 0)
                solver.add(c == registers[a] / b)
            case 'eql':
                solver.add(c == z3.If(registers[a] == b, one, zero))
        registers[a] = c
    solver.add(registers['z'] == 0)

##########
# part 1 #
##########
    solver.push()
    solver.maximize(sum((10 ** i) * d for i, d in enumerate(digits[::-1])))
    solver.check()
    m = solver.model()
    print(''.join([str(m[d]) for d in digits]))
    solver.pop()

##########
# part 2 #
##########
    solver.push()
    solver.minimize(sum((10 ** i) * d for i, d in enumerate(digits[::-1])))
    solver.check()
    m = solver.model()
    print(''.join([str(m[d]) for d in digits]))
    solver.pop()
