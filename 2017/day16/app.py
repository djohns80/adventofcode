import os

PROGRAMS = "abcdefghijklmnop"
DANCES = 1_000_000_000


def parse_moves(text):
    moves = []
    for move in text.strip().split(","):
        kind = move[0]
        if kind == "s":
            moves.append((kind, int(move[1:])))
        elif kind == "x":
            position_a, position_b = move[1:].split("/")
            moves.append((kind, int(position_a), int(position_b)))
        else:
            name_a, name_b = move[1:].split("/")
            moves.append((kind, name_a, name_b))
    return moves


def perform_moves(programs, moves):
    line = list(programs)
    for move in moves:
        kind = move[0]
        if kind == "s":
            size = move[1]
            line = line[-size:] + line[:-size]
        elif kind == "x":
            position_a, position_b = move[1], move[2]
            line[position_a], line[position_b] = line[position_b], line[position_a]
        else:
            position_a = line.index(move[1])
            position_b = line.index(move[2])
            line[position_a], line[position_b] = line[position_b], line[position_a]
    return "".join(line)


def dance(programs, moves, dances=1):
    # there are only so many possible orders, so repeating the dance must
    # eventually bring back an order already seen; from then on it cycles,
    # so the final order can be looked up instead of dancing every time
    orders = [programs]  # orders[n] is the order after n dances
    dances_done_when_seen = {programs: 0}
    order = programs
    for dances_done in range(1, dances + 1):
        order = perform_moves(order, moves)
        if order in dances_done_when_seen:
            cycle_start = dances_done_when_seen[order]
            cycle_length = dances_done - cycle_start
            return orders[cycle_start + (dances - cycle_start) % cycle_length]
        dances_done_when_seen[order] = dances_done
        orders.append(order)
    return order


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    moves = parse_moves(content)

    ##########
    # part 1 #
    ##########
    part_1 = dance(PROGRAMS, moves)
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = dance(PROGRAMS, moves, DANCES)
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
