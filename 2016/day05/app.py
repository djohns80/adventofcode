import argparse
import os
import hashlib

def main(input_file):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), input_file), 'r', encoding='utf-8')
    door_id = file.read().strip()

##########
# part 1 #
##########
#    n = 1
#    password = ''
#    while len(password) < 8:
#        door_hash = hashlib.md5((f'{door_id}{n}').encode('utf-8')).hexdigest()
#        if door_hash.startswith('0'*5):
#            password += door_hash[5]
#        n += 1
#    print(password)

##########
# part 2 #
##########
    n = 1
    password = {}
    while len(password.keys()) < 8:
        door_hash = hashlib.md5((f'{door_id}{n}').encode('utf-8')).hexdigest()
        if door_hash.startswith('0'*5) and door_hash[5] in '01234567':
            if door_hash[5] not in password:
                password[door_hash[5]] = door_hash[6]
        n += 1
    password_str = sorted(password.items())
    print(''.join([v[1] for v in password_str]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--input', action='store_const', dest='input', const='input')
    group.add_argument('-s', '--sample', action='store_const', dest='input', const='sample')
    parser.set_defaults(input='input')
    args = parser.parse_args()
    main(args.input)
