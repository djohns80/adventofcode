def index(x, y, is_light):
    i = 0
    for ny in range(y - 1, y + 2):
        for nx in range(x - 1, x + 2):
            i = i << 1 | is_light(nx, ny)
    return i

def enhance(light, step):
    xmin = min(x for x, _ in light)
    xmax = max(x for x, _ in light)
    ymin = min(y for _, y in light)
    ymax = max(y for _, y in light)

    def is_light(x, y):
        if algorithm[0] and not (xmin <= x <= xmax and ymin <= y <= ymax):
            return step % 2
        return (x, y) in light

    return {(x, y) for y in range(ymin - 1, ymax + 2)
            for x in range(xmin - 1, xmax + 2)
            if algorithm[index(x, y, is_light)]}

def enhance_times(light, times):
    for step in range(times):
        light = enhance(light, step)
    return light

#from collections import Counter
#
#def get_pixel(data, c):
#    temp = ''
#    for y in [-1,0,1]:
#        for x in [-1,0,1]:
#            if 0 <= c[1]+y < len(data) and 0 <= c[0]+x < len(data[0]):
#                temp += data[c[1]+y][c[0]+x]
#            else:
#                temp += '.'
#    bin_value = temp.replace('.','0').replace('#','1')
#    dec_value = int(bin_value, 2)
#    return algorithm[dec_value]
#
#def pad_input(data, i=1):
#    temp = ['.'*(len(data[0])+(2*i))]*i
#    temp.extend([f'{"."*i}{r}{"."*i}' for r in data])
#    temp.extend(['.'*(len(data[0])+(2*i))]*i)
#    return temp.copy()
#
#def process_image(data):
#    data = pad_input(data)
#    return [''.join([get_pixel(data, (x,y)) for x in range(len(r))]) for y,r in enumerate(data)].copy()

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.read()
    algorithm, input = lines.split('\n\n')
    algorithm = [c == '#' for c in algorithm]
    input = set([(x,y) for y,l in enumerate(input.splitlines()) for x,c in enumerate(l) if c == '#'])

##########
# part 1 #
##########
#    for _ in range(2):
#        input = process_image(input)
#    print(Counter([c for r in input for c in r])['#'])

    print(len(enhance_times(input, 2)))

##########
# part 2 #
##########
    print(len(enhance_times(input, 50)))
