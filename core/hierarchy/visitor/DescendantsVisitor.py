# DescendantsVisitor.py

from collections import defaultdict

from core.hierarchy.visitor.TopologicalVisitor import TopologicalVisitor


class DescendantsVisitor(TopologicalVisitor):
    def __init__(self, hierarchy):
        super().__init__(hierarchy)
        self.descendants = defaultdict(set)

    def visit(self, node):
        node_descendants = set(self.hierarchy.get_children(node))

        for child in node_descendants:
            node_descendants.update(self.descendants[child])

        self.descendants[node] = node_descendants

    def get_descendants(self):
        return self.descendants

    def get_descendant_counts(self):
        descendant_counts = {}
        for node, descendants in self.descendants.items():
            descendant_counts[node] = len(descendants)
        return descendant_counts
