file = open('input', 'r')
Lines = file.readlines()

###########
## part 1 #
###########
horizontal = 0
depth = 0
for line in Lines:
  action, value = line.strip().split(' ')
  value = int(value)
  if action == 'down':
    depth += value
  elif action == 'up':
    depth -= value
  elif action == 'forward':
    horizontal += value
print(horizontal * depth)

###########
## part 2 #
###########
horizontal = 0
depth = 0
aim = 0
for line in Lines:
  action, value = line.strip().split(' ')
  value = int(value)
  if action == 'down':
    aim += value
  elif action == 'up':
    aim -= value
  elif action == 'forward':
    horizontal += value
    depth += (aim * value)
print(horizontal * depth)
