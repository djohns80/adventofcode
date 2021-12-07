if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    input = file.read()

    lantern_fish = [int(i) for i in input.split(',')]
    fish_counts = [0]*9

    for fish in lantern_fish:
        fish_counts[fish] += 1

###########
## part 1 #
###########
    for d in range(80):
        new_fish = fish_counts[0]
        for i in range(len(fish_counts)-1):
            fish_counts[i] = fish_counts[i+1]
        fish_counts[8] = new_fish
        fish_counts[6] += new_fish
    print(sum(fish_counts))

###########
## part 2 #
###########
    for d in range(256):
        new_fish = fish_counts[0]
        for i in range(len(fish_counts)-1):
            fish_counts[i] = fish_counts[i+1]
        fish_counts[8] = new_fish
        fish_counts[6] += new_fish
    print(sum(fish_counts))
