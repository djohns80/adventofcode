import re

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

##########
# part 1 #
##########
    mem = {}
    mask = None
    for line in lines:
        if line.startswith('mask'):
            mask_match = re.search(r'mask\s=\s([X0-1]+)', line)
            mask = mask_match[1]
        elif line.startswith('mem'):
            mem_match = re.search(r'mem\[(\d+)\]\s=\s(\d+)', line)
            mem_address = int(mem_match[1])
            mem_value = f'{int(mem_match[2]):036b}'
            result = ['']*len(mask)
            for b in range(len(mask)):
                if mask[b] == 'X':
                    result[b] = mem_value[b]
                else:
                    result[b] = mask[b]
            mem[mem_address] = int(''.join(result), 2)
    print(sum([t for t in mem.values()]))

##########
# part 2 #
##########
    mem = {}
    mask = None
    for line in lines:
        if line.startswith('mask'):
            mask_match = re.search(r'mask\s=\s([X0-1]+)', line)
            mask = mask_match[1]
        elif line.startswith('mem'):
            mem_match = re.search(r'mem\[(\d+)\]\s=\s(\d+)', line)
            mem_address = f'{int(mem_match[1]):036b}'
            mem_value = int(mem_match[2])
            result = ['']*len(mask)
            for b in range(len(mask)):
                if mask[b] == '0':
                    result[b] = mem_address[b]
                else:
                    result[b] = mask[b]
            pop_addresses = [''.join(result)]
            final_addresses = []
            while len(pop_addresses) > 0:
                temp = pop_addresses.pop()
                if 'X' not in temp:
                    final_addresses.append(int(temp, 2))
                else:
                    pos = temp.find('X')
                    pop_addresses.append(f'{temp[:pos]}0{temp[pos+1:]}')
                    pop_addresses.append(f'{temp[:pos]}1{temp[pos+1:]}')
            for f in final_addresses:
                mem[f] = mem_value
    print(sum([t for t in mem.values()]))
