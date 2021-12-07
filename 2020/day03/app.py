import functools

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

##########
# part 1 #
##########
    route = (3,1)
    position = (0,0)
    squares = []
    while position[1] < len(lines)-1:
        position = (position[0] + route[0], position[1] + route[1])
        squares.append(lines[position[1]][position[0] % len(lines[0])])
    print(len([s for s in squares if s == '#']))

##########
# part 2 #
##########
    routes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    route_trees = []
    for route in routes:
        position = (0,0)
        squares = []
        while position[1] < len(lines)-1:
            position = (position[0] + route[0], position[1] + route[1])
            squares.append(lines[position[1]][position[0] % len(lines[0])])
        route_trees.append(len([s for s in squares if s == '#']))
    print(functools.reduce(lambda a, b: a*b, route_trees))
