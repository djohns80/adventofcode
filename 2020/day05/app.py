import re

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

##########
# part 1 #
##########
    seat_ids = []
    for l in lines:
        lower = 0
        upper = 127
        for fb in l[0:7]:
            half = int((upper-lower+1)/2)
            if fb == 'F':
                upper = upper - half
            elif fb == 'B':
                lower = lower + half
        row = lower
        lower = 0
        upper = 7
        for lr in l[7:]:
            half = int((upper-lower+1)/2)
            if lr == 'L':
                upper = upper - half
            elif lr == 'R':
                lower = lower + half
        col = lower
        seat_ids.append((row * 8) + col)
    print(max(seat_ids))

##########
# part 2 #
##########
    missing_seat_ids = list(set([i for i in range(128 * 8)]) - set(seat_ids))
    non_sequential = []
    for i in range(len(missing_seat_ids)):
        if i == 0:
            if missing_seat_ids[i] + 1 !=  missing_seat_ids[i+1]:
                non_sequential.append(missing_seat_ids[i])
        elif i == len(missing_seat_ids) - 1:
            if missing_seat_ids[i-1] + 1 != missing_seat_ids[i]:
                non_sequential.append(missing_seat_ids[i])
        elif missing_seat_ids[i-1]+1 != missing_seat_ids[i] and missing_seat_ids[i]+1 != missing_seat_ids[i+1]:
            non_sequential.append(missing_seat_ids[i])
    print(non_sequential)
