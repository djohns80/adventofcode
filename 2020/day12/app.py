if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]
    directions = [{'action': l[0], 'value': int(l[1:])} for l in lines]

###########
## part 1 #
###########
    east = 10
    north = 1
    facing = 0
    for d in directions:
        if d['action'] == 'N': # means to move north by the given value.
            north += d['value']
        elif d['action'] == 'S': # means to move south by the given value.
            north -= d['value']
        elif d['action'] == 'E': # means to move east by the given value.
            east += d['value']
        elif d['action'] == 'W': # means to move west by the given value.
            east -= d['value']
        elif d['action'] == 'L': # means to turn left the given number of degrees.
            facing -= int(d['value'] / 90)
            facing = facing % 4
        elif d['action'] == 'R': # means to turn right the given number of degrees.
            facing += int(d['value'] / 90)
            facing = facing % 4
        elif d['action'] == 'F': # means to move forward by the given value in the direction the ship is currently facing
            if facing == 0:
                east += d['value']
            elif facing == 2:
                east -= d['value']
            elif facing == 3:
                north += d['value']
            elif facing == 1:
                north -= d['value']
    print(abs(east) + abs(north))

###########
## part 1 #
###########
    w_east = 10
    w_north = 1
    s_east = 0
    s_north = 0
    for d in directions:
        if d['action'] == 'N':
            w_north += d['value']
        elif d['action'] == 'S':
            w_north -= d['value']
        elif d['action'] == 'E':
            w_east += d['value']
        elif d['action'] == 'W':
            w_east -= d['value']
        elif d['action'] == 'L':
            for t in range(int(d['value'] / 90)):
                temp = w_north
                w_north = w_east
                w_east = -temp
        elif d['action'] == 'R':
            for t in range(int(d['value'] / 90)):
                temp = w_north
                w_north = -w_east
                w_east = temp
        elif d['action'] == 'F':
            s_east += (w_east * d['value'])
            s_north += (w_north *d['value'])

    print(abs(s_east) + abs(s_north))