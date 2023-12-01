
def cast_spell(s, b, p):
    print(f"Player casts {s['name']}.")
    b['hp'] -= s['damage']
    if b['hp'] <= 0:
        print('This kills the boss, and the player wins.')
        return 1
    p['hp'] += s['hp']
    if s['effect']:
        p['effects'].append({'name': s['name'], **s['effect'].copy()})
    p['mana'] -= s['mana']
    return 0

def apply_effects(b, p):
    for e in p['effects']:
        p['armor'] = e['armor']
        p['mana'] += e['mana']
        b['hp'] -= e['damage']
        e['duration'] -= 1
        if e['damage'] > 0:
            print(f"{e['name']} deals {e['damage']} damage; its timer is now {e['duration']}.")
    if b['hp'] <= 0:
        print('This kills the boss, and the player wins.')
        return 1
    p['effects'] = [e for e in p['effects'] if e['duration'] > 0]
    return 0

def player_turn(b, p, s):
    print(f"- Player has {p['hp']} hit points, {p['armor']} armor, {p['mana']} mana")
    print(f"- Boss has {b['hp']} hit points")
    if apply_effects(b, p) != 0:
        return apply_effects(b, p)
    return cast_spell(s, b, p)

def boss_turn(b, p):
    print(f"- Player has {p['hp']} hit points, {p['armor']} armor, {p['mana']} mana")
    print(f"- Boss has {b['hp']} hit points")
    if apply_effects(b, p) != 0:
        return apply_effects(b, p)
    print(f"Boss attacks for {(b['damage'] - p['armor'])} damage.")
    p['hp'] -= (b['damage'] - p['armor'])
    if p['hp'] <= 0:
        print('This kills the player, and the boss wins.')
        return -1
    return 0

def main():
    boss = {
#        'hp': 51,
        'hp': 14,
        'mana': 0,
#        'damage': 9,
        'damage': 8,
        'armor': 0
    }

    spells = [
#    Magic Missile costs 53 mana. It instantly does 4 damage.
        {
            'name': 'Magic Missle',
            'mana': 53,
            'damage': 4,
            'hp': 0,
            'effect': None
        },
#    Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
        {
            'name': 'Drain',
            'mana': 73,
            'damage': 2,
            'hp': 2,
            'effect': None
        },
#    Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
        {
            'name': 'Shield',
            'mana': 113,
            'damage': 0,
            'hp': 0,
            'effect': {
                'duration': 5,   # 6
                'armor': 7,
                'damage': 0,
                'mana': 0
            }
        },
#    Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
        {
            'name': 'Poison',
            'mana': 173,
            'damage': 0,
            'hp': 0,
            'effect': {
                'duration': 6,
                'armor': 0,
                'damage': 3,
                'mana': 0
            }
        },
#    Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
        {
            'name': 'Recharge',
            'mana': 229,
            'damage': 0,
            'hp': 0,
            'effect': {
                'duration': 5,
                'armor': 0,
                'damage': 0,
                'mana': 101
            }
        }
    ]

##########
# part 1 #
##########
    ### TODO: complete part 1
    player = {
#        'hp': 50,
#        'mana': 500,
        'hp': 10,
        'mana': 250,
        'damage': 0,
        'armor': 0,
        'effects': []
    }

    spell_list = [0,3,1,2,4]

    while True:
        print('-- Player turn --')
        if player_turn(boss, player, spells[spell_list.pop()]) != 0:
            break
        print()
        print('-- Boss turn --')
        if boss_turn(boss, player) != 0:
            break
        print()




#    print('-- Player turn --')
#    player_turn(boss, player, spells[2])
#    print()

#    print('-- Boss turn --')
#    boss_turn(boss, player)
#    print()

#    print(player)



# Poison deals 3 damage; its timer is now 5.
# Boss attacks for 8 damage.

# -- Player turn --
# - Player has 2 hit points, 0 armor, 77 mana
# - Boss has 10 hit points
# Poison deals 3 damage; its timer is now 4.
# Player casts Magic Missile, dealing 4 damage.

# -- Boss turn --
# - Player has 2 hit points, 0 armor, 24 mana
# - Boss has 3 hit points
# Poison deals 3 damage. This kills the boss, and the player wins




##########
# part 2 #
##########
    ### TODO: complete part 2


if __name__ == '__main__':
    main()
