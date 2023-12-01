from collections import defaultdict
import itertools

def win_battle(p_hp, p_d, p_a, b_hp, b_d, b_a):
    while True:
        b_hp -= (p_d - b_a)
        if b_hp <= 0:
            return True
        p_hp -= (b_d - p_a)
        if p_hp <= 0:
            return False

def main():
    boss = {
        'HP': 104,
        'Damage': 8,
        'Armor': 1
    }

    shop_lines = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""
    shop = defaultdict(list)
    for l in shop_lines.strip().splitlines():
        if l == '':
            continue
        elif ':' in l:
            header = l.replace(':', '').split()
        else:
            item = l.split()
            shop[header[0]].append({ header[1]: int(item[-3]), header[2]: int(item[-2]), header[3]: int(item[-1])})

    equipment_options = [(w, a, r1, r2) for w in shop['Weapons'] for a in (shop['Armor'] + [{'Cost': 0, 'Damage': 0, 'Armor': 0}]) for r1, r2 in itertools.combinations(shop['Rings'] + ([{'Cost': 0, 'Damage': 0, 'Armor': 0}] * 2), 2)]

##########
# part 1 #
##########
    min_cost = 9999
    for o in equipment_options:
        stats = {k: sum(i[k] for i in o) for k in o[0].keys()}
        if win_battle(100, stats['Damage'], stats['Armor'], boss['HP'], boss['Damage'], boss['Armor']):
            if stats['Cost'] < min_cost:
                min_cost = stats['Cost']
    print(min_cost)

##########
# part 2 #
##########
    ### TODO: complete part 2
    max_cost = 0
    for o in equipment_options:
        stats = {k: sum(i[k] for i in o) for k in o[0].keys()}
        if not win_battle(100, stats['Damage'], stats['Armor'], boss['HP'], boss['Damage'], boss['Armor']):
            if stats['Cost'] > max_cost:
                max_cost = stats['Cost']
    print(max_cost)

if __name__ == '__main__':
    main()
