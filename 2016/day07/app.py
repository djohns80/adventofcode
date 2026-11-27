import os


def split_address(address):
    # returns (supernet parts, hypernet parts); hypernet parts are inside [ ]
    supernets = []
    hypernets = []
    current = ""
    for char in address:
        if char == "[":
            supernets.append(current)
            current = ""
        elif char == "]":
            hypernets.append(current)
            current = ""
        else:
            current += char
    supernets.append(current)
    return supernets, hypernets


def has_abba(text):
    for i in range(len(text) - 3):
        a, b, c, d = text[i : i + 4]
        if a == d and b == c and a != b:
            return True
    return False


def supports_tls(address):
    supernets, hypernets = split_address(address)
    for hypernet in hypernets:
        if has_abba(hypernet):
            return False
    for supernet in supernets:
        if has_abba(supernet):
            return True
    return False


def find_abas(text):
    # returns every three-character sequence like "xyx" (outer characters
    # equal, middle character different)
    abas = []
    for i in range(len(text) - 2):
        a, b, c = text[i : i + 3]
        if a == c and a != b:
            abas.append(text[i : i + 3])
    return abas


def supports_ssl(address):
    supernets, hypernets = split_address(address)
    for supernet in supernets:
        for aba in find_abas(supernet):
            # the matching BAB swaps the outer and middle characters
            bab = aba[1] + aba[0] + aba[1]
            for hypernet in hypernets:
                if bab in hypernet:
                    return True
    return False


def main():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
    lines = content.splitlines()

    ##########
    # part 1 #
    ##########
    part_1 = 0
    for address in lines:
        if supports_tls(address):
            part_1 += 1
    print("part 1:", part_1)

    ##########
    # part 2 #
    ##########
    part_2 = 0
    for address in lines:
        if supports_ssl(address):
            part_2 += 1
    print("part 2:", part_2)


if __name__ == "__main__":
    main()
