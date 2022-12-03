import re

def parse_input(data):
    capture_mode = 'rules'
    results = {
        'rules': {},
        'messages': []
    }
    for line in data:
        if line == '':
            capture_mode = 'messages'
        elif capture_mode == 'rules':
            k, _, v = line.partition(': ')
            results['rules'][k] = v
        elif capture_mode == 'messages':
            results['messages'].append(line)
    return results

def get_re(s):
    if s == '|':
        return s
    rule_s = input['rules'][s]
    if rule_s.startswith('"'):
        return rule_s.strip('"')
    else:
        return f'({"".join(get_re(part) for part in rule_s.split())})'

if __name__ == '__main__':
#   file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

    input = parse_input(lines)

##########
# part 1 #
##########
#    full_matches = [m for m in input['messages'] if re.fullmatch(get_re('0'), m)]
#    print(len(full_matches))

##########
# part 2 #
##########
    re_42 = re.compile(get_re('42'))
    re_31 = re.compile(get_re('31'))
    matches = 0
    for m in input['messages']:
        pos = 0
        count_42 = 0
        while match := re_42.match(m, pos):
            count_42 += 1
            pos = match.end()

        count_31 = 0
        while match := re_31.match(m, pos):
            count_31 += 1
            pos = match.end()

        if 0 < count_31 < count_42 and pos == len(m):
            matches += 1
    print(matches)
