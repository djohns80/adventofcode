def get_loop_size(keys, subject_number, d):
    value = 1
    n = 1
    while True:
        value = (value * subject_number) % d
        if value in keys:
            return (value, n)
        n += 1

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    pks = [int(l.strip()) for l in lines]

##########
# part 1 #
##########
    loop = get_loop_size(pks, 7, 20201227)
    pk = [pk for pk in pks if pk != loop[0]][0]
    print(pow(pk, loop[1], 20201227))
