import os

def main():
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'input'), 'r', encoding='utf-8')
    elves = file.read().split('\n\n')
    elf_calories = {n: [int(c) for c in elf.split('\n') if c != ''] for n, elf in enumerate(elves)}

##########
# part 1 #
##########
    elf_calories_sum  = {k: sum(v) for k,v in elf_calories.items()}
    print(max(elf_calories_sum.values()))

##########
# part 2 #
##########
    sorted_elf_calories = sorted(elf_calories_sum.items(), key=lambda kv: kv[1], reverse=True)
    print(sum(dict(sorted_elf_calories[:3]).values()))

if __name__ == '__main__':
    main()
