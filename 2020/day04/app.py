import re

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    data = file.read().split('\n\n')

##########
# part 1 #
##########
    passports = [{f.split(':')[0]: f.split(':')[1] for f in ' '.join(p.splitlines()).split(' ')} for p in data]
    fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'] #, 'cid']
    valid = [p for p in passports if set(fields).issubset(set(p.keys()))]
    print(len(valid))

##########
# part 2 #
##########
    invalid = []
    for p in valid:
        for k,v in p.items():
            if k == 'byr' and not re.match(r'^19[2-9][0-9]|200[0-2]$', v):
                invalid.append(p)
                break
            elif k == 'iyr' and not re.match(r'^201[0-9]|2020$', v):
                invalid.append(p)
                break
            elif k == 'eyr' and not re.match(r'^202[0-9]|2030$', v):
                invalid.append(p)
                break
            elif k == 'hgt' and not re.match(r'^(1[5-8][0-9]|19[0-3])cm|(59|6[0-9]|7[0-6])in$', v):
                invalid.append(p)
                break
            elif k == 'hcl' and not re.match(r'^#[0-9a-f]{6}$', v):
                invalid.append(p)
                break
            elif k == 'ecl' and not re.match(r'^amb|blu|brn|gry|grn|hzl|oth$', v):
                invalid.append(p)
                break
            elif k == 'pid' and not re.match(r'^\d{9}$', v):
                invalid.append(p)
                break
    print(len(valid) - len(invalid))
