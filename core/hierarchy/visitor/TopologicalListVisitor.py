# TopologicalListVisitor.py

from collections import deque

from core.hierarchy.visitor.TopologicalVisitor import TopologicalVisitor


class TopologicalListVisitor(TopologicalVisitor):
    def __init__(self, hierarchy):
        super().__init__(hierarchy)
        self.result = []

    def visit(self, node):
        self.result.append(node)

    def get_topological_list(self):
        return self.result
