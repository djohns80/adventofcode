import os
from collections import defaultdict


def get_neighbours(candidate_plots, neighbours=set()):
    plot = candidate_plots.pop()
    neighbours.add(plot)
    neighbours.update(
        [candidate for candidate in candidate_plots if abs(plot - candidate) == 1]
    )
    outsiders = [
        candidate for candidate in candidate_plots if candidate not in neighbours
    ]
    # next_neighbour = neighbours.pop()
    # for neighbour in neighbours:
    #     get_neighbours(next_neighbour, outsiders, neighbours)
    return list(neighbours), outsiders


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    content = file.read().strip()
    lines = [line.strip() for line in content.splitlines()]
    plot_grid = defaultdict(list)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            plot_grid[char].append(x + y * 1j)

    plot_groups = []
    for plant, plots in plot_grid.items():
        while plots:
            group = [plots.pop()]
            added = 1
            while added > 0:
                added = 0
                neighbours = set([p for g in group for p in plots if abs(g - p) == 1])
                group.extend(neighbours)
                for n in neighbours:
                    added += 1
                    plots.remove(n)
            plot_groups.append((plant, group))

    part_1 = 0
    part_2 = 0
    for _, plot_group in plot_groups:
        permimeter = 0
        sides = 0
        # for x, y in plot_group:
        for plot in plot_group:
            # Perimeter
            permimeter += 4 - sum(abs(plot - p) == 1 for p in plot_group)
            # Outer corners
            sides += (plot - 1) not in plot_group and (plot - 1j) not in plot_group
            sides += (plot + 1) not in plot_group and (plot - 1j) not in plot_group
            sides += (plot - 1) not in plot_group and (plot + 1j) not in plot_group
            sides += (plot + 1) not in plot_group and (plot + 1j) not in plot_group
            # Inner corners
            sides += (
                (plot - 1) in plot_group
                and (plot - 1j) in plot_group
                and (plot - 1 - 1j) not in plot_group
            )
            sides += (
                (plot + 1) in plot_group
                and (plot - 1j) in plot_group
                and (plot + 1 - 1j) not in plot_group
            )
            sides += (
                (plot - 1) in plot_group
                and (plot + 1j) in plot_group
                and (plot - 1 + 1j) not in plot_group
            )
            sides += (
                (plot + 1) in plot_group
                and (plot + 1j) in plot_group
                and (plot + 1 + 1j) not in plot_group
            )
        part_1 += len(plot_group) * permimeter
        part_2 += len(plot_group) * sides

    ##########
    # part 1 #
    ##########
    print(part_1)

    # ##########
    # # part 2 #
    # ##########
    print(part_2)


if __name__ == "__main__":
    main()
