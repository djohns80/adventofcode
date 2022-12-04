import argparse
import os
import re
from datetime import datetime
from itertools import groupby
from collections import defaultdict, Counter

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    lines = file.read().strip().split('\n')
    events = []
    for l in lines:
        match = re.match(r'^\[(?P<datetime>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})\]\s(?P<activity>falls asleep|wakes up|Guard #(?P<guard>\d+) begins shift)$', l)
        if match:
            events.append({
                **match.groupdict(),
                'datetime': datetime.strptime(match.groupdict()['datetime'], '%Y-%m-%d %H:%M')
            })
    events = sorted(events, key=lambda e: e['datetime'])

##########
# part 1 #
##########
    on_shift = None
    start = None
    sleeping = []
    for e in events:
        if e['guard']:
            on_shift = e['guard']
        elif e['activity'] == 'falls asleep':
            start = e['datetime']
        elif e['activity'] == 'wakes up':
            sleeping.append({
                'guard': on_shift,
                'date': start.strftime('%m-%d'),
                'minutes': range(start.minute, e['datetime'].minute),
                'duration': len(range(start.minute, e['datetime'].minute))
            })

    sleeping = sorted(sleeping, key=lambda s: s['guard'])

    total_sleeping = [(k, sum([s['duration'] for s in v])) for k,v in groupby(sleeping, key=lambda s: s['guard'])]
    total_sleeping = sorted(total_sleeping, key=lambda s: s[1], reverse=True)

    sleeping_ranges = [s['minutes'] for s in sleeping if s['guard'] == total_sleeping[0][0]]

    common_minutes = defaultdict(int)
    for sr in sleeping_ranges:
        for n in sr:
            common_minutes[n] += 1
    common_minutes = sorted(common_minutes.items(), key=lambda s: s[1], reverse=True)
    print(int(total_sleeping[0][0]) * common_minutes[0][0])

##########
# part 2 #
##########
    guard_minutes = [(s['guard'], n) for s in sleeping for n in s['minutes']]
    guard_minute = Counter(guard_minutes).most_common(1)[0][0]
    print(int(guard_minute[0]) * guard_minute[1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
