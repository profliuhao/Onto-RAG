# LowestCommonAncestorVisitor.py
from collections import defaultdict

from core.hierarchy.visitor.TopologicalVisitor import TopologicalVisitor


class LowestCommonAncestorVisitor(TopologicalVisitor):
    def __init__(self, hierarchy, starting_points):
        super().__init__(hierarchy)
        self.starting_points = starting_points
        self.subhierarchy_points = defaultdict(int)
        self.ancestors = set()

    def visit(self, node):
        count = 1 if node in self.starting_points else 0
        for child in self.hierarchy.get_children(node):
            count += self.subhierarchy_points[child]

        self.subhierarchy_points[node] = count
        if count == len(self.starting_points):
            self.ancestors.add(node)

    def get_lowest_common_ancestors(self):
        return self.ancestors
