import numpy

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    input = file.readlines()

    values = [int(i.strip()) for i in input]

##########
# part 1 #
##########
    numbers = [(v1, v2) for v1i, v1 in enumerate(values) for v2i, v2 in enumerate(values) if v2i > v1i and v1 + v2 == 2020]
    print(numbers[0], numpy.prod(numbers[0]))

##########
# part 2 #
##########
    numbers = [(v1, v2, v3) for v1i, v1 in enumerate(values) for v2i, v2 in enumerate(values) for v3i, v3 in enumerate(values) if v3i > v2i > v1i and v1 + v2 + v3 == 2020]
    print(numbers[0], numpy.prod(numbers[0]))
