import json

file = open('125843.json', 'r')
data = json.loads(file.read())

for m_id, member in data['members'].items():
    data = member['name']
    for d in range(5):
        if str(d+1) in member['completion_day_level']:
            for p in range(2):
                if str(p+1) in member['completion_day_level'][str(d+1)]:
                    data = data + '\t' + str(member['completion_day_level'][str(d+1)][str(p+1)]['get_star_ts'])
                else:
                    data = data + '\t'
        else:
            data = data + '\t' + '\t'
    print(data)