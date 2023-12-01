import argparse
import os
import re

#https://github.com/llimllib/personal_code/blob/master/misc/advent/2022/16/a.py

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
#    data = [m.groupdict() for m in re.finditer(r'Valve\s(?P<in>[A-Z]{2})\shas\sflow\srate=(?P<rate>\d+);\stunnels?\sleads?\sto\svalves?\s(?P<out>(?:[A-Z]{2}(?:, )?)+(?:[A-Z]{2})?)', file.read())]
#    valves = {d['in']: {'rate': int(d['rate']), 'out': d['out'].split(', ')} for d in data}

    s = file.read()
    valves = {}

    for line in s.splitlines():
        parts = line.split()
        valve = parts[1]
        flow_rate = int(parts[4][5:-1])
        lead_to = ''.join(parts[9:]).split(',')
        valves[valve] = (flow_rate, lead_to)

    valve_to_num = {}
    for key in sorted(valves.keys()):
        valve_to_num[key] = 1 << len(valve_to_num)

    valves = {
        valve_to_num[valve]: (flow_rate, tuple(map(valve_to_num.get, lead_to)))
        for valve, (flow_rate, lead_to) in valves.items()
    }



    TOTAL_TIME = 30

    states = [(valve_to_num['AA'], 0, 0)]

    best = {}

    for t in range(1, TOTAL_TIME+1):
#        print(t, len(states))

        new_states = []
        for loc, opened, pressure in states:
            key = (loc, opened)
            if key in best and pressure <= best[key]:
                continue

            best[key] = pressure

            flow_rate, lead_to = valves[loc]
            if loc & opened == 0 and flow_rate > 0:
                new_states.append((loc, opened | loc, pressure + flow_rate * (TOTAL_TIME - t)))
            for dest in lead_to:
                new_states.append((dest, opened, pressure))

        states = new_states

#    answer = max(pressure for _, _, pressure in states)

    print(states)

##########
# part 1 #
##########
#    position = 'AA'
#    open_valves = []
#    pressure = 0
#    steps = ['DD', 'o', 'CC', 'BB', 'o', 'AA', 'II', 'JJ', 'o', 'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'o', 'GG', 'FF', 'EE', 'o', 'DD', 'CC', 'o', None, None, None, None, None, None]
#    for s in steps:
#        pressure += sum(valves[v]['rate'] for v in open_valves)
#        if s == 'o':
#            open_valves.append(position)
#        elif s:
#            position = s
#    print(pressure)

##########
# part 2 #
##########


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
