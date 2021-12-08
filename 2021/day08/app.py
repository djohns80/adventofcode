def decode_unique(data):
    len_2_1 = [u for u in data if len(u) == 2][0]
    len_4_4 = [u for u in data if len(u) == 4][0]
    len_3_7 = [u for u in data if len(u) == 3][0]
    len_7_8 = [u for u in data if len(u) == 7][0]
    len_5 = [u for u in data if len(u) == 5]
    diff_8_4 = set(list(len_7_8)) - set(list(len_4_4))
    len_5_2 = [s for s in len_5 if diff_8_4 <= set(list(s))][0]
    len_5.remove(len_5_2)
    len_5_5 = [s for s in len_5 if len(set(list(s)) - set(list(len_5_2))) == 2][0]
    len_5.remove(len_5_5)
    len_5_3 = len_5[0]
    len_6 = [u for u in data if len(u) == 6]
    len_6_6 = [s for s in len_6 if not set(list(s)) >= set(list(len_2_1))][0]
    len_6.remove(len_6_6)
    len_6_0 = [s for s in len_6 if list(set(list(len_6_6)) - set(list(len_5_5)))[0] in s][0]
    len_6.remove(len_6_0)
    len_6_9 = len_6[0]
    return {
        len_6_0: 0,
        len_2_1: 1,
        len_5_2: 2,
        len_5_3: 3,
        len_4_4: 4,
        len_5_5: 5,
        len_6_6: 6,
        len_3_7: 7,
        len_7_8: 8,
        len_6_9: 9
    }

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

###########
## part 1 #
###########
    count = 0
    for line in lines:
        unique_signals = line.split('|')[0].strip().split(' ')
        output_value = line.split('|')[1].strip().split(' ')
        count += len([t for t in output_value if len(t) in [2,4,3,7]])
    print(count)

###########
## part 2 #
###########
    sum = 0
    for line in lines:
        unique_signals = line.split('|')[0].strip().split(' ')
        unique_signals = [''.join(sorted(list(u))) for u in unique_signals]
        output_values = line.split('|')[1].strip().split(' ')
        output_values = [''.join(sorted(list(o))) for o in output_values]

        codes = decode_unique(unique_signals)
        value = int(''.join([str(codes[o]) for o in output_values]))
        sum += value
    print(sum)
