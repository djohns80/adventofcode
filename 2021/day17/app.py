import re

if __name__ == '__main__':
#    input = 'target area: x=20..30, y=-10..-5'
    input = 'target area: x=57..116, y=-198..-148'

    p = {k:int(v) for k,v in re.search(r'target\sarea:\sx=(?P<min_x>\d+)..(?P<max_x>\d+),\sy=(?P<min_y>-?\d+)..(?P<max_y>-?\d+)', input).groupdict().items()}

##########
# part 1 #
##########
    targets = {}
    for vxi in range(1, p['max_x']+1):
        for vyi in range(p['min_y'], p['max_x']-p['max_y']):
            x = 0
            y = 0
            max_h = 0
            vx = vxi
            vy = vyi
            while vx > 0 or y > p['min_y']:
                x = x + vx
                y = y + vy
                max_h = max(max_h, y)
                vx = max(0, vx - 1)
                vy = vy - 1
                if p['min_x'] <= x <= p['max_x'] and p['min_y'] <= y <= p['max_y']:
                    targets[(vxi, vyi)] = max_h
                    break
    print(max(targets.values()))

##########
# part 2 #
##########
    print(len(targets))
