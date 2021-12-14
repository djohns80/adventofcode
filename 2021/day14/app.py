from collections import defaultdict

def complete_step():
    temp = defaultdict(int)
    for pair in pair_counts:
        temp[pair[0] + rules[pair]] += pair_counts[pair]
        temp[rules[pair] + pair[1]] += pair_counts[pair]
    return temp

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    data = file.read()
    template, rules = data.split('\n\n')
    template = template.strip()
    rules = [s.strip().split(' -> ') for s in rules.splitlines()]
    rules = {s[0]: s[1] for s in rules}

    pair_counts = defaultdict(int)
    for c in range(len(template) - 1):
        pair_counts[template[c:c+2]] += 1

##############
# part 1 & 2 #
##############
    for s in range(40):
        pair_counts = complete_step()
        if s == 10-1 or s == 40-1:
            element_counts = defaultdict(int)
            for k,v in pair_counts.items():
                element_counts[k[0]] += v
            element_counts[template[-1]] += 1
            sorted_counts = sorted(element_counts.values())
            print(sorted_counts[-1] - sorted_counts[0])
