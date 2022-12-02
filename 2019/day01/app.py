import math

def fuel(mass):
    amt = math.floor(mass / 3) - 2
    return 0 if amt < 0 else amt

def recursive_fuel(m):
    f = 0
    while fuel(m) > 0:
        f += fuel(m)
        m = fuel(m)
    return f

if __name__ == '__main__':
    file = open('input', 'r', encoding='utf-8')
    modules = [int(m.strip()) for m in file.readlines()]

##########
# part 1 #
##########
    fuel_reqs_1 = [fuel(m) for m in modules]
    print(sum(fuel_reqs_1))

##########
# part 2 #
##########
    fuel_reqs_2 = [recursive_fuel(m) for m in modules]
    print(sum(fuel_reqs_2))
