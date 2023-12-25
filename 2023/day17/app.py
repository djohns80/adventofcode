import os
import math
from collections import defaultdict
import utils.direction as direc
import utils.graph as graph


def main():
    file = open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "input"),
        "r",
        encoding="utf-8",
    )
    lines = map(str.strip, file.readlines())

    ##########
    # part 1 #
    ##########
    # g = tuple(tuple(map(int, tuple(line))) for line in lines)
    # nodes = []
    # m = len(g)
    # edges = defaultdict(list)
    # for y1, gy in enumerate(g):
    #     for x1 in range(len(gy)):
    #         for d in (direc.LEFT, direc.RIGHT, direc.UP, direc.DOWN):
    #             for n in range(4):
    #                 node = (y1, x1, d, n)
    #                 nodes.append(node)
    #                 if n < 3:
    #                     if 0 <= y1 + d[0] <= m - 1 and 0 <= x1 + d[1] <= m - 1:
    #                         edges[node].append(
    #                             graph.Edge(
    #                                 (y1 + d[0], x1 + d[1], d, n + 1),
    #                                 g[y1 + d[0]][x1 + d[1]],
    #                             )
    #                         )
    #                 ld = direc.turn_left(d)
    #                 rd = direc.turn_right(d)
    #                 if 0 <= y1 + rd[0] <= m - 1 and 0 <= x1 + rd[1] <= m - 1:
    #                     edges[node].append(
    #                         graph.Edge(
    #                             (y1 + rd[0], x1 + rd[1], rd, 1),
    #                             g[y1 + rd[0]][x1 + rd[1]],
    #                         )
    #                     )
    #                 if 0 <= y1 + ld[0] <= m - 1 and 0 <= x1 + ld[1] <= m - 1:
    #                     edges[node].append(
    #                         graph.Edge(
    #                             (y1 + ld[0], x1 + ld[1], ld, 1),
    #                             g[y1 + ld[0]][x1 + ld[1]],
    #                         )
    #                     )
    # g = graph.Graph(nodes, edges)
    # dist, _ = g.dijkstra((0, 0, direc.RIGHT, 0))
    # b = math.inf
    # for k, v in dist.items():
    #     if k[0] == m - 1 and k[1] == m - 1:
    #         b = min(b, v)
    # print(b)

    ##########
    # part 2 #
    ##########
    g = tuple(tuple(map(int, tuple(line))) for line in lines)
    nodes = []
    my = len(g)
    mx = len(g[0])
    edges = defaultdict(list)
    for y1, gy in enumerate(g):
        for x1 in range(len(gy)):
            for d in (direc.LEFT, direc.RIGHT, direc.UP, direc.DOWN):
                for n in range(11):
                    node = (y1, x1, d, n)
                    nodes.append(node)
                    if n < 10:
                        if 0 <= y1 + d[0] <= my - 1 and 0 <= x1 + d[1] <= mx - 1:
                            edges[node].append(
                                graph.Edge(
                                    (y1 + d[0], x1 + d[1], d, n + 1),
                                    g[y1 + d[0]][x1 + d[1]],
                                )
                            )
                    ld = direc.turn_left(d)
                    rd = direc.turn_right(d)
                    if n >= 4:
                        if 0 <= y1 + rd[0] <= my - 1 and 0 <= x1 + rd[1] <= mx - 1:
                            edges[node].append(
                                graph.Edge(
                                    (y1 + rd[0], x1 + rd[1], rd, 1),
                                    g[y1 + rd[0]][x1 + rd[1]],
                                )
                            )
                        if 0 <= y1 + ld[0] <= my - 1 and 0 <= x1 + ld[1] <= mx - 1:
                            edges[node].append(
                                graph.Edge(
                                    (y1 + ld[0], x1 + ld[1], ld, 1),
                                    g[y1 + ld[0]][x1 + ld[1]],
                                )
                            )
    g = graph.Graph(nodes, edges)
    dist, _ = g.dijkstra((0, 0, direc.RIGHT, 0))
    dist2, _ = g.dijkstra((0, 0, direc.DOWN, 0))
    b = math.inf
    for k, v in dist.items():
        if k[0] == my - 1 and k[1] == mx - 1 and k[-1] >= 4:
            b = min(b, v)
    for k, v in dist2.items():
        if k[0] == my - 1 and k[1] == mx - 1 and k[-1] >= 4:
            b = min(b, v)
    print(b)


if __name__ == "__main__":
    main()
