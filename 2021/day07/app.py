import statistics

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    input = file.read()

    horiz_crab = [int(i) for i in input.split(',')]

##########
# part 1 #
##########
    median = int(statistics.median(horiz_crab))
    fuel = [abs(median-h) for h in horiz_crab]
    print(sum(fuel))

##########
# part 2 #
##########
    results = []
    for x in range(min(horiz_crab), max(horiz_crab)+1):
        fuel = [abs(x-h)*(1+abs(x-h))/2 for h in horiz_crab]
        results.append((x, sum(fuel)))
    results.sort(key=lambda tup: tup[1])
    print(int(results[0][1]))
