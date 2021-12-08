import copy

def execute_boot(code):
    executed = [False]*len(code)
    acc = 0
    line_no = 0
    while line_no < len(code):
        if executed[line_no]:
            break
        else:
            executed[line_no] = True
        if code[line_no]['operation'] == 'acc':
            acc += code[line_no]['argument']
            line_no += 1
        elif code[line_no]['operation'] == 'jmp':
            line_no += code[line_no]['argument']
        elif code[line_no]['operation'] == 'nop':
            line_no += 1
    return line_no != len(code), acc

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

##########
# part 1 #
##########
    instructions = [{'operation': line.split(' ')[0], 'argument': int(line.split(' ')[1])} for line in lines]
    infinite, result = execute_boot(instructions)
    print(result)
###########
## part 1 #
###########
    for n,i in enumerate(instructions):
        instructions_temp = copy.deepcopy(instructions)
        if i['operation'] == 'jmp':
            instructions_temp[n]['operation'] = 'nop'
        elif i['operation'] == 'nop':
            instructions_temp[n]['operation'] = 'jmp'
        infinite, result = execute_boot(instructions_temp)
        if not infinite:
            print(result)
            break
