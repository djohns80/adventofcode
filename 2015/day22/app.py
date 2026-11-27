import heapq
import os

PLAYER_HP = 50
PLAYER_MANA = 500

# effect timers are stored as a tuple indexed by these positions
SHIELD, POISON, RECHARGE = 0, 1, 2

# name, cost, instant damage, heal, effect index, effect turns
SPELLS = [
    ("Magic Missile", 53, 4, 0, None, 0),
    ("Drain", 73, 2, 2, None, 0),
    ("Shield", 113, 0, 0, SHIELD, 6),
    ("Poison", 173, 0, 0, POISON, 6),
    ("Recharge", 229, 0, 0, RECHARGE, 5),
]


def start_of_turn(boss_hp, mana, timers):
    """Apply active effects, then tick their timers down. Returns the armor in force this turn."""
    armor = 7 if timers[SHIELD] else 0
    if timers[POISON]:
        boss_hp -= 3
    if timers[RECHARGE]:
        mana += 101
    return boss_hp, mana, armor, tuple(max(t - 1, 0) for t in timers)


def least_mana_to_win(boss_hp, boss_damage, player_hp, mana, hard=False):
    # Dijkstra on mana spent: the first winning state popped is the cheapest win
    queue = [(0, player_hp, mana, boss_hp, (0, 0, 0))]
    seen = set()
    while queue:
        spent, hp, mana, boss_hp, timers = heapq.heappop(queue)
        if boss_hp <= 0:
            return spent
        state = (hp, mana, boss_hp, timers)
        if state in seen:
            continue
        seen.add(state)

        # player turn
        if hard:
            hp -= 1
            if hp <= 0:
                continue
        boss_hp, mana, _, timers = start_of_turn(boss_hp, mana, timers)
        if boss_hp <= 0:
            heapq.heappush(queue, (spent, hp, mana, boss_hp, timers))
            continue
        for _, cost, damage, heal, effect, turns in SPELLS:
            if cost > mana or (effect is not None and timers[effect]):
                continue
            new_timers = timers
            if effect is not None:
                new_timers = timers[:effect] + (turns,) + timers[effect + 1 :]
            new_hp = hp + heal
            new_mana = mana - cost
            new_boss_hp = boss_hp - damage

            # boss turn
            if new_boss_hp > 0:
                new_boss_hp, new_mana, armor, new_timers = start_of_turn(
                    new_boss_hp, new_mana, new_timers
                )
                if new_boss_hp > 0:
                    new_hp -= max(boss_damage - armor, 1)
                    if new_hp <= 0:
                        continue
            heapq.heappush(
                queue, (spent + cost, new_hp, new_mana, new_boss_hp, new_timers)
            )
    return None


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    boss = {}
    for line in lines:
        stat, value = line.split(":", 1)
        boss[stat] = int(value)

    ##########
    # part 1 #
    ##########
    part_1 = least_mana_to_win(
        boss["Hit Points"], boss["Damage"], PLAYER_HP, PLAYER_MANA
    )
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = least_mana_to_win(
        boss["Hit Points"], boss["Damage"], PLAYER_HP, PLAYER_MANA, hard=True
    )
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
