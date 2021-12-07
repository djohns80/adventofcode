import re

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = [m.groupdict() for m in re.finditer(r'(?P<start_range>\d+)-(?P<end_range>\d+)\s(?P<letter>[a-z]):\s(?P<password>[a-z]+)', file.read())]

##########
# part 1 #
##########
    valid = [line for line in lines if int(line['end_range']) >= len(line['password'])-len(line['password'].replace(line['letter'],'')) >= int(line['start_range'])]
    print(len(valid))

##########
# part 2 #
##########
    valid = [line for line in lines if bool(line['password'][int(line['start_range'])-1] == line['letter']) != bool(line['password'][int(line['end_range'])-1] == line['letter'])]
    print(len(valid))
