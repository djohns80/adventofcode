import argparse
import os
import re
import math
from collections import defaultdict

ORE, CLAY, OBSIDIAN, GEODE = 1, 2, 3, 4
MATERIALS = [ORE, CLAY, OBSIDIAN, GEODE]

def largest_for_blueprint(b, end_time):
    init_robots = {m: 0 for m in MATERIALS}
    init_robots[ORE] = 1
    stack = [(0, init_robots, {m: 0 for m in MATERIALS}, set())]
    best_at_time = defaultdict(int)
    max_robots = get_max_robots(b)
    while stack:
        t, robots, resources, skipped_last_iteration = stack.pop(0)
        best_at_time[t] = max(best_at_time[t], resources[GEODE])
        if t <= end_time and best_at_time[t] == resources[GEODE]:
            options = get_build_options(b, resources)
            for to_build in options:
                if not to_build:
                    resources1 = harvest(robots, resources.copy())
                    stack.append((t + 1, robots, resources1, options))
                elif to_build in skipped_last_iteration:
                    continue
                elif robots[to_build] + 1 > max_robots[to_build]:
                    continue
                else:
                    robots1, resources1 = build_robot(
                        b, robots.copy(), resources.copy(), to_build)
                    resources1 = harvest(robots, resources1.copy())
                    stack.insert(0, (t + 1, robots1, resources1, set()))
    return best_at_time[end_time]

def get_max_robots(b):
    max_robots = {m: 0 for m in MATERIALS}
    max_robots[GEODE] = 100
    for _, needs in b.items():
        for robot, qty in needs.items():
            max_robots[robot] = max(max_robots[robot], qty)
    return max_robots

def get_build_options(b, resources):
    options = {0}
    for robot, needs in b.items():
        if all(qty <= resources[need] for need, qty in needs.items()):
            options.add(robot)
    if GEODE in options:
        return {GEODE}
    return options

def build_robot(b, robots, resources, to_build):
    robots[to_build] += 1
    for resource, qty in b[to_build].items():
        resources[resource] -= qty
        assert resources[resource] >= 0
    return (robots, resources)

def harvest(robots, resources):
    for k, v in robots.items():
        resources[k] += v
    return resources

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    blueprints = {int(b.groupdict()['id']): {
            ORE: {
                ORE: int(b.groupdict()['ore_ore'])
            },
            CLAY: {
                ORE: int(b.groupdict()['clay_ore'])
            },
            OBSIDIAN: {
                ORE: int(b.groupdict()['obsidian_ore']),
                CLAY: int(b.groupdict()['obsidian_clay']),
            },
            GEODE: {
                ORE: int(b.groupdict()['geode_ore']),
                OBSIDIAN: int(b.groupdict()['geode_obsidian'])
            }
        } for b in re.finditer(r'Blueprint\s(?P<id>\d+):\sEach\sore\srobot\scosts\s(?P<ore_ore>\d+)\sore\.\sEach\sclay\srobot\scosts\s(?P<clay_ore>\d+)\sore\.\sEach\sobsidian\srobot\scosts\s(?P<obsidian_ore>\d+)\sore\sand\s(?P<obsidian_clay>\d+)\sclay\.\sEach\sgeode\srobot\scosts\s(?P<geode_ore>\d+)\sore\sand\s(?P<geode_obsidian>\d+)\sobsidian\.', file.read())}

##########
# part 1 #
##########
    print(sum(i * largest_for_blueprint(b, 24) for i, b in blueprints.items()))

##########
# part 2 #
##########
    print(math.prod(largest_for_blueprint(b, 32) for b in list(blueprints.values())[:3]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
