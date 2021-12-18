import re

def snailfish_maths(numbers):
    expr = numbers.pop(0)
    while numbers:
        expr = f'[{expr},{numbers.pop(0)}]'
        old_sum = None
        while old_sum != expr:
            old_sum = expr
            exploded = False
            for m in re.finditer(r'\[\d+,\d+\]',expr):
                a,b = [int(d) for d in m.group()[1:-1].split(',')]
                prefix = expr[:m.start()]
                suffix = expr[m.end():]
                depth = len(prefix.replace(']','')) - len(prefix.replace('[',''))
                if depth == 4:
                    prefix, suffix = get_explode((a,b), prefix, suffix)
                    expr = f'{prefix}0{suffix}'
                    exploded = True
                    break
            if not exploded:
                split = re.search(r'\d\d+',expr)
                if split:
                    expr = f'{expr[:split.start()]}{get_split(split.group())}{expr[split.end():]}'
    return expr

def get_magnitude(number):
    while '[' in number:
        for m in re.finditer(r'\[\d+,\d+\]',number):
            a,b = [int(d) for d in m.group()[1:-1].split(',')]
            number = number.replace(m.group(), str(3*a + 2*b))
    return int(number)

def get_split(regular):
    v = int(regular)
    return f'[{v//2},{v-(v//2)}]'

def get_explode(pair, pre, suf):
    pre_m = re.search(r'\d+',pre[::-1])
    if pre_m:
        pre = f'{pre[:len(pre) - pre_m.end()]}{str(int(pre_m.group()[::-1]) + pair[0])}{pre[len(pre) - pre_m.start():]}'
    suf_m = re.search(r'\d+',suf)
    if suf_m:
        suf = f'{suf[:suf_m.start()]}{str(int(suf_m.group()) + pair[1])}{suf[suf_m.end():]}'
    return pre, suf

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

##########
# part 1 #
##########
    final_number = snailfish_maths(lines.copy())
    print(get_magnitude(final_number))

##########
# part 1 #
##########
    number_pairs = [(l1,l2) for l1 in lines for l2 in lines if l1 != l2]
    max_magnitude = 0
    for n1, n2 in number_pairs:
        magnitude = get_magnitude(snailfish_maths([n1, n2]))
        if magnitude > max_magnitude:
            max_magnitude = magnitude
    print(max_magnitude)
