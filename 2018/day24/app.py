import os
import re
from dataclasses import dataclass, replace

IMMUNE_SYSTEM = "Immune System"
GROUP_PATTERN = re.compile(
    r"(\d+) units each with (\d+) hit points (?:\((.*)\) )?"
    r"with an attack that does (\d+) (\w+) damage at initiative (\d+)"
)


# eq=False so groups compare by identity: two groups with identical stats are still different groups
@dataclass(eq=False)
class Group:
    army: str
    number: int  # 1-based position within its army, as used in the puzzle's battle log
    units: int
    hit_points: int
    attack_damage: int
    attack_type: str
    initiative: int
    weaknesses: frozenset
    immunities: frozenset

    @property
    def effective_power(self):
        return self.units * self.attack_damage


def parse_armies(lines):
    """Parse both armies into a single list of groups."""
    groups = []
    army = None
    number = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith(":"):
            army = line[:-1]
            number = 0
            continue
        match = GROUP_PATTERN.fullmatch(line)
        units, hit_points, traits, attack_damage, attack_type, initiative = (
            match.groups()
        )
        weaknesses = set()
        immunities = set()
        if traits:
            # e.g. "weak to fire; immune to cold, slashing"
            for trait in traits.split("; "):
                kind, damage_types = trait.split(" to ")
                if kind == "weak":
                    weaknesses.update(damage_types.split(", "))
                else:
                    immunities.update(damage_types.split(", "))
        number += 1
        groups.append(
            Group(
                army=army,
                number=number,
                units=int(units),
                hit_points=int(hit_points),
                attack_damage=int(attack_damage),
                attack_type=attack_type,
                initiative=int(initiative),
                weaknesses=frozenset(weaknesses),
                immunities=frozenset(immunities),
            )
        )
    return groups


def damage_dealt(attacker, defender):
    """Damage the attacker would deal the defender right now, ignoring how many units the defender has."""
    if attacker.attack_type in defender.immunities:
        return 0
    if attacker.attack_type in defender.weaknesses:
        return 2 * attacker.effective_power
    return attacker.effective_power


def select_targets(groups):
    """Target selection phase: return a list of (attacker, defender) pairs."""
    selection_order = sorted(
        groups,
        key=lambda group: (group.effective_power, group.initiative),
        reverse=True,
    )
    already_targeted = set()
    pairs = []
    for attacker in selection_order:
        best_target = None
        best_key = None
        for defender in groups:
            if defender.army == attacker.army or defender in already_targeted:
                continue
            damage = damage_dealt(attacker, defender)
            if damage == 0:
                continue
            # most damage, then largest effective power, then highest initiative
            key = (damage, defender.effective_power, defender.initiative)
            if best_key is None or key > best_key:
                best_target = defender
                best_key = key
        if best_target is not None:
            already_targeted.add(best_target)
            pairs.append((attacker, best_target))
    return pairs


def fight_round(groups):
    """Run one fight (target selection then attacking), updating units in place. Returns the units killed."""
    pairs = select_targets(groups)
    pairs.sort(key=lambda pair: pair[0].initiative, reverse=True)
    total_killed = 0
    for attacker, defender in pairs:
        if attacker.units <= 0:
            # it was wiped out earlier in this round
            continue
        # damage is recalculated here because the attacker may have lost units this round
        killed = damage_dealt(attacker, defender) // defender.hit_points
        killed = min(killed, defender.units)
        defender.units -= killed
        total_killed += killed
    return total_killed


def total_units(groups):
    total = 0
    for group in groups:
        total += group.units
    return total


def battle(groups, boost=0):
    """
    Fight until only one army remains, adding boost to the immune system's attack damage.
    Returns (winning army, units it has left), or (None, units left on both sides) on a stalemate.
    The groups passed in are not modified.
    """
    fighting = []
    for group in groups:
        attack_damage = group.attack_damage
        if group.army == IMMUNE_SYSTEM:
            attack_damage += boost
        fighting.append(replace(group, attack_damage=attack_damage))

    while True:
        armies = set()
        for group in fighting:
            armies.add(group.army)
        if len(armies) == 1:
            return armies.pop(), total_units(fighting)

        killed = fight_round(fighting)
        if killed == 0:
            # nothing changed, so every later round would be identical: it would never end
            return None, total_units(fighting)

        survivors = []
        for group in fighting:
            if group.units > 0:
                survivors.append(group)
        fighting = survivors


def smallest_winning_boost(groups):
    """
    Try boosts 0, 1, 2, ... until the immune system wins. Returns (boost, units it has left).
    Boosts are tried one by one rather than by binary search because a bigger boost doesn't
    always help: one boost can win while a slightly bigger one ends in a stalemate.
    """
    boost = 0
    while True:
        winner, units_left = battle(groups, boost)
        if winner == IMMUNE_SYSTEM:
            return boost, units_left
        boost += 1


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()
    groups = parse_armies(lines)

    ##########
    # part 1 #
    ##########
    _, part_1 = battle(groups)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    _, part_2 = smallest_winning_boost(groups)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
