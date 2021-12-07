if __name__ == '__main__':
    file = open('input', 'r')
    Lines = file.readlines()

##########
# part 1 #
##########
    previous_value = None
    increase_count = 0
    for line in Lines:
        current_value = int(line.strip())
        if previous_value is not None:
            if current_value > previous_value:
                increase_count += 1
        previous_value = current_value
    print(increase_count)

##########
# part 2 #
##########
    previous_value = None
    increase_count = 0
    for n in range(2, len(Lines)):
        current_value = int(Lines[n-2].strip()) + int(Lines[n-1].strip()) + int(Lines[n].strip())
        if previous_value is not None:
            if current_value > previous_value:
                increase_count += 1
        previous_value = current_value
    print(increase_count)
