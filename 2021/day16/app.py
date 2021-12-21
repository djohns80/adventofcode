import math

def literal_packet(message):
    out = ''
    for i in range(6, len(message), 5):
        out += message[i+1:i+5]
        if message[i] == '0':
            break
    return out, i + 5

def decode(message):
    version = int(message[:3], 2)
    type_id = int(message[3:6], 2)
    if type_id == 4:
        out, length = literal_packet(message)
        value = [out]
    else:
        value = []
        length_type = int(message[6])
        if length_type == 0:
            length = 7 + 15 + int(message[7:7+15], 2)
            offset = 7 + 15
            while offset + 6 <= length:
                v, val, o = decode(message[offset:length])
                version += v
                value.append(val)
                offset += o
        elif length_type == 1:
            subpackets = int(message[7:7+11], 2)
            length = 7 + 11
            for _ in range(subpackets):
                v, val, o = decode(message[length:])
                version += v
                value.append(val)
                length += o

    if type_id == 0:
        value = sum(value)
    elif type_id == 1:
        value = math.prod(value)
    elif type_id == 2:
        value = min(value)
    elif type_id == 3:
        value = max(value)
    elif type_id == 4:
        value = int(value[0], 2)
    elif type_id == 5:
        value = int(value[0] > value[1])
    elif type_id == 6:
        value = int(value[0] < value[1])
    elif type_id == 7:
        value = int(value[0] == value[1])

    return version, value, length

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    data = file.read().strip()

    packet = ''.join([f'{int(h, 16):04b}' for h in data])
    part1, part2, _  = decode(packet)

##########
# part 1 #
##########
    print(part1)

##########
# part 2 #
##########
    print(part2)
