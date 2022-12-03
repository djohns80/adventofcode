import os

def common_items(lists):
    common = lists[0]
    for l in lists[1:]:
        common = ''.join(set(common).intersection(set(l)))
    return common

def priority(item):
    if item.islower():
        return ord(item) - (ord('a') - 1)
    else:
        return ord(item) - (ord('A') - 27)

def main():
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'input'), 'r', encoding='utf-8')
    rucksacks = file.read().strip().split('\n')

##########
# part 1 #
##########
    compartments = [[r[:int(len(r)/2)], r[int(len(r)/2):]] for r in rucksacks]
    compartments_common = [common_items(c) for c in compartments]
    compartments_priorities = [priority(cc) for cc in compartments_common]
    print(sum(compartments_priorities))

##########
# part 2 #
##########
    groups = [rucksacks[i:i+3] for i in range(0, len(rucksacks), 3)]
    groups_common = [common_items(c) for c in groups]
    groups_priorities = [priority(cc) for cc in groups_common]
    print(sum(groups_priorities))

if __name__ == '__main__':
    main()
