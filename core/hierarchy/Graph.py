# Graph.py

from collections import defaultdict

from core.hierarchy.Edge import Edge


class Graph:
    def __init__(self, edges=None):
        self.outgoing_edges = {}
        self.incoming_edges = {}

        if edges:
            for edge in edges:
                self.add_edge(edge)

    def add_node(self, node):
        if node not in self.outgoing_edges:
            self.outgoing_edges[node] = set()
        if node not in self.incoming_edges:
            self.incoming_edges[node] = set()

    def add_edge(self, edge):
        self.add_edge_by_nodes(edge.source, edge.target)

    def add_edge_by_nodes(self, from_node, to_node):
        self.add_node(from_node)
        self.add_node(to_node)

        self.outgoing_edges[from_node].add(to_node)
        self.incoming_edges[to_node].add(from_node)

    def get_incoming_edges(self, node):
        return self.incoming_edges.get(node, set())

    def get_outgoing_edges(self, node):
        return self.outgoing_edges.get(node, set())

    def get_nodes(self):
        return set(self.outgoing_edges.keys())

    def get_edges(self):
        edges = set()

        for node, adjacent_nodes in self.outgoing_edges.items():
            edges.update(Edge(node, adjacent_node) for adjacent_node in adjacent_nodes)

        return edges

    def contains_node(self, node):
        return node in self.incoming_edges

    def contains_edge(self, edge):
        return edge.source in self.outgoing_edges and edge.target in self.outgoing_edges[edge.source]

