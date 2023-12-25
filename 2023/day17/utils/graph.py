#!/usr/bin/env python3

from collections import defaultdict, Counter
import copy
import math
import utils.heap as heap


class Graph:
    """A class for representing basic graphs, with nodes and edges.

    Methods:
    dijsktra(start_node): Calculates the shortest paths to every reachable node in the graph from the start
    topo_sort()"""

    def __init__(self, nodes, adjacencies):
        self.nodes = nodes
        self.adj = adjacencies

    def dijkstra(self, start_node):
        nodes = self.nodes
        adj = self.adj
        dist = {start_node: 0}
        prev = {}
        queue = heap.HeapQueue()
        queue.insert(start_node, 0)

        for n in nodes:
            if n != start_node:
                dist[n] = math.inf
                prev[n] = None
                queue.insert(n, dist[n])

        while queue.len() > 0:
            smallest = queue.pop()
            for edge in adj[smallest]:
                new_dist = dist[smallest] + edge.cost
                if new_dist < dist[edge.dest]:
                    dist[edge.dest] = new_dist
                    prev[edge.dest] = smallest
                    queue.remove(edge.dest)
                    queue.insert(edge.dest, new_dist)
        return dist, prev

    def topo_sort(self, in_edges=None, key_sorter=lambda k: k):
        if in_edges is not None:
            if set(self.nodes) != set(in_edges.keys()):
                raise ValueError("Provided in-edge counts do not match graph nodes")
        nodes = self.nodes
        adj = self.adj
        if in_edges is None:
            in_edges = Counter()
            for node in nodes:
                if in_edges[node] == 0:
                    in_edges[
                        node
                    ] = 0  # Ensure the value exists, for iteration purposes
                for adjacent_edge in adj[node]:
                    in_edges[adjacent_edge.dest] += 1
        out = []
        while len(out) < len(nodes):
            new_in_edges = in_edges.copy()
            options = []
            for node, ies in in_edges.items():
                if ies == 0:
                    options.append(node)
            options.sort(key=key_sorter)
            node = options.pop(0)
            out.append(node)
            del new_in_edges[node]
            for adjacent_edge in adj[node]:
                new_in_edges[adjacent_edge.dest] -= 1
            in_edges = new_in_edges
        return out

    def all_topo_sorts(self, in_edges=None):
        nodes = self.nodes
        adj = self.adj
        if in_edges is None:
            in_edges = Counter()
            for node in nodes:
                try:
                    for adjacent_edge in adj[node]:
                        in_edges[adjacent_edge.dest] += 1
                except:
                    pass
            for node in nodes:
                if node not in in_edges.keys():
                    in_edges[node] = 0
        if len(in_edges) == 0:
            return [[]]
        out = []
        for node, ies in in_edges.items():
            if ies == 0:
                new_in_edges = in_edges.copy()
                del new_in_edges[node]
                try:
                    for adjacent_edge in adj[node]:
                        new_in_edges[adjacent_edge.dest] -= 1
                except:
                    pass
                all_opts = self.all_topo_sorts(new_in_edges)
                new_all_opts = []
                if len(all_opts) > 0:
                    for opt in all_opts:
                        op2 = opt.copy()
                        op2.insert(0, node)
                        new_all_opts.append(op2)
                else:
                    new_all_opts = [[node]]
                for opt in new_all_opts:
                    out.append(opt)
        return out

    def simplify_graph(self, important):
        nodes = self.nodes
        adj = self.adj
        new_adj = defaultdict(list)
        for node in important:
            if node not in nodes:
                raise ValueError(f"Node '{node}' in important not in original graph")
        for n1 in important:
            dist, prev = self.dijkstra(n1)
            for n2 in important:
                if n1 == n2:
                    continue
                if dist[n2] == math.inf:
                    continue
                curr_node = n2
                while curr_node == n2 or curr_node not in important:
                    curr_node = prev[curr_node]
                if curr_node == n1:
                    new_adj[n1].append(Edge(n2, dist[n2]))
        return Graph(important, new_adj)

    def rename_graph(self, node_mapping):
        new_adj = defaultdict(list)
        new_nodes = []
        for node in self.nodes:
            new_curr = []
            for edge in self.adj[node]:
                new_curr.append(Edge(node_mapping[edge.dest], edge.cost))
            new_node = node_mapping[node]
            new_adj[new_node] = new_curr
            new_nodes.append(new_node)
        return Graph(new_nodes, new_adj)

    def remove_node(self, node):
        # Currently doesn't fix up links, but assumes there's no paths that strictly go through the removed node
        # Reason: lazy
        nodes = self.nodes.copy()
        adj = copy.deepcopy(self.adj)
        nodes.remove(node)
        del adj[node]
        for k, v in adj.items():
            for idx, edge in enumerate(v):
                if edge.dest == node:
                    del v[idx]
        return Graph(nodes, adj)

    def connected_components(self):
        nodes = self.nodes
        edges = self.adj
        nodes_known = 0
        components = {}
        for node in nodes:
            if nodes_known == len(nodes):
                break
            if node in components.keys():
                continue
            curr_node = node
            start_node = node
            components[node] = start_node
            queue = edges[node].copy()
            seen = set()
            while len(queue) > 0:
                curr_node = queue.pop().dest
                if curr_node in seen:
                    continue
                components[curr_node] = start_node
                nodes_known += 1
                seen.add(curr_node)
                queue.extend(edges[curr_node])
        return components

    def floyd_warshall(self):  # not yet tested
        dist = defaultdict(dict)
        prev = defaultdict(dict)
        nodes = self.nodes
        edges = self.adj
        for node in nodes:
            for edge in edges[node]:
                other = edge.dest
                dist[node][dest] = edge.cost
                prev[node][dest] = node
        for node in nodes:
            dist[node][node] = 0
            prev[node][node] = node
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                for k in range(len(self.nodes)):
                    if dist[j][k] > dist[j][i] + dist[i][k]:
                        dist[j][k] = dist[j][i] + dist[i][k]
                        prev[j][k] = prev[i][k]

        return dist, prev

    def __str__(self):
        return str(self.nodes) + "\n" + str(self.adj)

    def __repr__(self):
        return str(self.nodes) + "\n" + str(self.adj)


class Edge:
    def __init__(self, dest, cost=0):
        self.dest = dest
        self.cost = cost

    def __str__(self):
        return f"(-> {self.dest}, {self.cost})"

    def __repr__(self):
        return f"(-> {self.dest}, {self.cost})"

    def __copy__(self):
        return Edge(self.dest.copy(), self.cost)

    def __deepcopy__(self, memo):
        return Edge(copy.deepcopy(self.dest), self.cost)
