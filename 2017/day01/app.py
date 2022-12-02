def index(i, l):
    return i if i < l else i-l

if __name__ == '__main__':
    file = open('input', 'r', encoding='utf-8')
    digits = [int(d) for d in list(file.read()) if d.strip() != '']

##########
# part 1 #
##########
    digit_matches = [digits[n] for n in range(len(digits)) if digits[n] == digits[index(n+1, len(digits))]]
    print(sum(digit_matches))

##########
# part 2 #
##########
    interval = int(len(digits)/2)
    digit_matches = [digits[n] for n in range(len(digits)) if digits[n] == digits[index(n + interval, len(digits))]]
    print(sum(digit_matches))
