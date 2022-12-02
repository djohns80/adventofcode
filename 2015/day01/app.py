if __name__ == '__main__':
    file = open('input', 'r', encoding='utf-8')
    instructions= list(file.read())

##########
# part 1 #
##########
    deltas = [1 if i == '(' else -1 for i in instructions]
    print(sum(deltas))

##########
# part 2 #
##########
    floor = 0
    for n, d in enumerate(deltas, 1):
        floor += d
        if floor == -1:
            print(n)
            break
