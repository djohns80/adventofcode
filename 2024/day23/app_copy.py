import os


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )

    edges = set(frozenset(v.split("-")) for v in file.read().splitlines())
    nodes = set(n for e in edges for n in e)
    extend = lambda groups: set(
        frozenset([*group, nn])
        for group in groups
        for nn in nodes
        if all(frozenset((nn, n)) in edges for n in group)
    )

    ##########
    # part 1 #
    ##########
    groups = extend(edges)
    print(sum(1 for g in groups if any(n[0] == "t" for n in g)))

    ##########
    # part 2 #
    ##########
    while ngroups := extend(groups):
        groups = ngroups
    print(",".join(sorted(list(groups)[0])))


if __name__ == "__main__":
    main()
