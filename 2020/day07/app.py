import re

def get_bags(data):
    result = {}
    for line in data:
        bag_and_contents_regex = r"^(\w+\s\w+)\sbags\scontain\s(.*)"
        bag_and_contents = re.search(bag_and_contents_regex, line)
        bag_type = bag_and_contents[1]
        contents_string = bag_and_contents[2][:-1]
        contents_regex = r'([0-9])\s+(\w+\s\w+)\sbag'
        contents_tuples = re.findall(contents_regex, contents_string)
        bag_contents = []
        for t in contents_tuples:
            if t[1] != 'no other':
                bag_contents.append({
                    'count': int(t[0]),
                    'type': t[1]
                })
        result[bag_type] = bag_contents
    return result

def bag_count(bag_collection, bag_name, part):
    count = 0
    bag = bag_collection[bag_name]
    if len(bag) == 0:
        return count
    else:
        for b in bag:
##########
# part 1 #
##########
            if part == 1:
                if b['type'] == 'shiny gold':
                    count += 1
                count += bag_count(bag_collection, b['type'], part)

###########
## part 2 #
###########
            elif part == 2:
                current_bag_type_count = b['count']
                count += current_bag_type_count
                bags_inside_current_bag_type_count = bag_count(bag_collection, b['type'], part)
                count += bags_inside_current_bag_type_count * current_bag_type_count
    return count

if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]
    bags = get_bags(lines)

##########
# part 1 #
##########
    print(len([b for b in bags if bag_count(bags, b, 1) > 0]))

##########
# part 2 #
##########
    print(bag_count(bags, 'shiny gold', 2))
