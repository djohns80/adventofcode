import copy

def _index(lst, val):
    try:
        return lst.index(val)
    except ValueError:
        return -1

def match_pairs(data):
    temp = ''
    for n in range(len(data)-1):
        pos_a = _index(opens,data[n])
        pos_b = _index(closes,data[n+1])
        if pos_b == -1:
            temp += data[n]
        elif pos_a != pos_b:
            temp += data[n+1:]
            return temp, (data[n], data[n+1])
        elif pos_a == pos_b:
            temp += data[n+2:]
            return temp, None
    return None, None

def complete_line(data):
    temp = ''
    for c in data:
        if c in opens:
            temp += c
        elif c in closes:
            temp = temp[0 : temp.rindex(opens[closes.index(c)])] + temp[temp.rindex(opens[closes.index(c)])+1:]
    return ''.join([closes[opens.index(c)] for c in temp[::-1]])

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

###########
## part 1 #
###########
    opens = ['(','[','{','<']
    closes = [')',']','}','>']
    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    incomplete_lines = copy.deepcopy(lines)
    wrongs = []
    for line in lines:
        orig_line = line
        while True:
            temp_line, mismatch = match_pairs(line)
            if temp_line is None or mismatch is not None:
                break
            else:
                line = temp_line
        if mismatch is not None:
            wrongs.append(mismatch[1])
            incomplete_lines.remove(orig_line)
    print(sum([points[w] for w in wrongs]))

###########
## part 2 #
###########
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }
    scores = []
    for line in incomplete_lines:
        score = 0
        for c in complete_line(line):
            score = (score * 5) + points[c]
        scores.append(score)
    print(sorted(scores)[len(scores) // 2])
