if __name__ == '__main__':
#    file = open('sample', 'r')
    file = open('input', 'r')
    groups = file.read().split('\n\n')

##########
# part 1 #
##########
    questions = [len(list(set(''.join(g.splitlines())))) for g in groups]
    print(sum(questions))

##########
# part 2 #
##########
    questions = 0
    for g in groups:
        common_questions = None
        for p in g.splitlines():
            if common_questions is None:
                common_questions = set(p)
            else:
                common_questions.intersection_update(set(p))
        questions += len(common_questions)
    print(questions)
