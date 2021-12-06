def parse_lines(data):
    numbers = []
    boards = []
    temp_board = []
    for line in data:
        if len(numbers) == 0:
            numbers = [int(v) for v in line.split(',')]
        else:
            if line == '':
                if temp_board != []:
                    boards.append(temp_board)
                    temp_board = []
            else:
                temp_board.append([(int(v), False) for v in line.split(' ') if v != ''])
    boards.append(temp_board)
    return numbers, boards

def update_boards(number, boards):
    for ib, b in enumerate(boards):
        for ir, r in enumerate(b):
            for ic, c in enumerate(r):
                if c[0] == number:
                    boards[ib][ir][ic] = (c[0], True)

def check_boards(boards):
    winning_boards = []
    for ib, b in enumerate(boards):
        if any([all([v[1] for v in r]) for r in b]) or any([all([b[ir][ic][1] for ir in range(len(b))]) for ic in range(len(b[0]))]):
            winning_boards.append(ib)
    return winning_boards

def play_bingo(data):
    numbers, boards = parse_lines(data)
    for n in numbers:
        update_boards(n, boards)
        winning_boards = check_boards(boards)
        winning_boards.sort(reverse=True)
        if len(winning_boards) != 0:
            for wb in winning_boards:
#                print(boards[wb])
                sum_unmarked = sum([c[0] for r in boards[wb] for c in r if not c[1]])
                print(n * sum_unmarked)
                boards.remove(boards[wb])
############
### part 1 #
############
#                return
###########
## part 2 #
###########
                if len(boards) == 0:
                    return

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

    play_bingo(lines)
