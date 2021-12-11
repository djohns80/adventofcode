if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    lines = file.readlines()
    lines = [l.strip() for l in lines]

##########
# part 1 #
##########
    all_ingredients = []
    all_allergens = {}
    for line in lines:
        i, a = line.strip(')').split(' (contains ')
        ingredients = i.split(' ')
        allergies = a.split(', ')
        all_ingredients.extend(ingredients)
        for allergen in allergies:
            if allergen in all_allergens:
                all_allergens[allergen] &= set(ingredients)
            else:
                all_allergens[allergen] = set(ingredients)
    allergen_foods = set([i for v in all_allergens.values() for i in v])
    safe_foods = [i for i in all_ingredients if i not in allergen_foods]
    print(len(safe_foods))

##########
# part 2 #
##########
    canonical = {}
    while all_allergens:
        known = [(k,list(v)[0]) for k,v in all_allergens.items() if len(v) == 1]
        for k,v in known:
            canonical[k] = v
            del all_allergens[k]
            for a in all_allergens:
                if v in all_allergens[a]:
                    all_allergens[a].remove(v)
    print(','.join([v for k,v in sorted(canonical.items())]))
