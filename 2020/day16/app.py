import math

def parse_input(data):
    capture_mode = 'rules'
    results = {
        'rules': {},
        'your_ticket': [],
        'nearby_tickets': []
    }
    for line in data:
        if line.endswith(':'):
            capture_mode = line[:-1].replace(' ','_')
        elif capture_mode == 'rules':
            line_split = line.split(':')
            results['rules'][line_split[0].replace(' ','_')] = [[int(n) for n in v.split('-')] for v in line_split[1].strip().split(' or ')]
        elif capture_mode == 'your_ticket':
            results['your_ticket'] = [int(v) for v in line.split(',')]
        elif capture_mode == 'nearby_tickets':
            results['nearby_tickets'].append([int(v) for v in line.split(',')])
    return results

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines if l.strip() != '']
    input = parse_input(lines)

##########
# part 1 #
##########
    invalid_values = [val for nt in input['nearby_tickets'] for val in nt if not any([rng[0] <= val <= rng[1] for rul in input['rules'].values() for rng in rul])]
    print(sum(invalid_values))

##########
# part 2 #
##########
    invalid_tickets = [nt for nt in input['nearby_tickets'] for val in nt if not any([rng[0] <= val <= rng[1] for rul in input['rules'].values() for rng in rul])]
    for it in invalid_tickets:
        input['nearby_tickets'].remove(it)

    matched_field_ids = {}
    for fid in range(len(input['nearby_tickets'][0])):
        cf = [nt[fid] for nt in input['nearby_tickets']]
        matched_field_ids[fid] = [rul for rul, rngs in input['rules'].items() if all([any([rng[0] <= val <= rng[1] for rng in rngs]) for val in cf])]

    while any([len(t) != 1 for t in matched_field_ids.values()]):
        for mfid1 in matched_field_ids:
            if len(matched_field_ids[mfid1]) == 1:
                match = matched_field_ids[mfid1][0]
                for mfid2 in matched_field_ids:
                    if mfid1 != mfid2:
                        matched_field_ids[mfid2] = [f for f in matched_field_ids[mfid2] if f != match]

    your_ticket = {}
    for fid, v in enumerate(input['your_ticket']):
        your_ticket[matched_field_ids[fid][0]] = v

    departure_values = [v for k, v in your_ticket.items() if k.startswith('departure')]
    print(math.prod(departure_values))
