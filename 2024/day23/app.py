import os
from itertools import combinations


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample"),
        "r",
        encoding="utf-8",
    )
    content = file.read()
    connections = [set(line.split("-")) for line in content.splitlines()]
    computers = set([c for connection in connections for c in connection])

    ##########
    # part 1 #
    ##########
    t_computers = [c for c in computers if c.startswith("t")]
    t_triplets = set()
    for t_c in t_computers:
        for t1, t2, t3 in combinations([t for t in computers if t != t_c], 3):
            if (
                set([t1, t2]) in connections
                and set([t1, t3]) in connections
                and set([t2, t3]) in connections
            ):
                t_triplets.add(frozenset([t1, t2, t3]))

    # for t1, t2, t3 in combinations(computers, 3):
    #     if t1.startswith("t") or t2.startswith("t") or t3.startswith("t"):
    #         if (
    #             set([t1, t2]) in connections
    #             and set([t1, t3]) in connections
    #             and set([t2, t3]) in connections
    #         ):
    #             count += 1
    #             # print(t1, t2, t3)
    print(len(t_triplets))


##########
# part 2 #
##########


if __name__ == "__main__":
    main()
