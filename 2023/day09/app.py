import os


def reduce_sequence(seq, reductions):
    seq_diff = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    reductions.append(seq_diff)
    if all([n == 0 for n in seq_diff]):
        return reductions
    else:
        return reduce_sequence(seq_diff, reductions)


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = map(str.split, map(str.strip, file.readlines()))
    sequences = [list(map(int, line)) for line in lines]

    ##########
    # part 1 #
    ##########
    part_1 = 0
    for s in sequences:
        diff_sequences = reduce_sequence(s, [s])
        diff_sequences[-1].append(0)
        for i in reversed(range(len(diff_sequences) - 1)):
            diff_sequences[i].append(diff_sequences[i][-1] + diff_sequences[i + 1][-1])
        part_1 += diff_sequences[0][-1]
    print(part_1)

    ##########
    # part 2 #
    ##########
    part_2 = 0
    for s in sequences:
        diff_sequences = reduce_sequence(s, [s])
        diff_sequences[-1] = [0] + diff_sequences[-1]
        for i in reversed(range(len(diff_sequences) - 1)):
            diff_sequences[i] = [
                diff_sequences[i][0] - diff_sequences[i + 1][0]
            ] + diff_sequences[i]
        part_2 += diff_sequences[0][0]
    print(part_2)


if __name__ == "__main__":
    main()
