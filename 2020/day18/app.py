import re

def evaluate(expr, part=1):
    re1 = re.search(r'(\d+).+', expr)
    expr = expr[len(re1[1]):]
    steps = [int(re1[1])]
    re2 = re.findall(r'([\+\*])(\d+)', expr)
    for r in re2:
        steps.extend([r[0], int(r[1])])
    if part == 1:
        answer = steps.pop(0)
        for s in range(0, len(steps), 2):
            if steps[s] == '+':
                answer += steps[s+1]
            elif steps[s] == '*':
                answer *= steps[s+1]
    if part == 2:
        answer = 0
        for s in range(len(steps)-2, 0, -2):
            if steps[s] == '+':
                steps[s-1] = steps[s-1] + steps[s+1]
                steps.pop(s+1)
                steps.pop(s)
        for s in range(len(steps)-2, 0, -2):
            if steps[s] == '*':
                steps[s-1] = steps[s-1] * steps[s+1]
                steps.pop(s+1)
                steps.pop(s)
        answer = steps[0]
    return answer

def brackets(expr, part=1):
    capture = ''
    capturing = None
    for i, c in enumerate(expr):
        if capturing is not None:
            if c == ')':
                return expr[:capturing] + str(evaluate(capture, part)) + expr[i+1:]
            elif c == '(':
                capture = ''
                capturing = i
            else:
                capture += c
        else:
            if c == '(':
                capture = ''
                capturing = i

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip().replace(' ' ,'') for l in lines if l.strip() != '']

##########
# part 1 #
##########
    values = []
    for line in lines:
        while '(' in line:
            line = brackets(line)
        values.append(evaluate(line))
    print(sum(values))

##########
# part 2 #
##########
    values = []
    for line in lines:
        while '(' in line:
            line = brackets(line, 2)
        values.append(evaluate(line, 2))
    print(sum(values))
