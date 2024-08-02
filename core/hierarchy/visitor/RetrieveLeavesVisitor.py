# RetrieveLeavesVisitor.py
from core.hierarchy.visitor.HierarchyVisitor import HierarchyVisitor
from typing import Set



class RetrieveLeavesVisitor(HierarchyVisitor):
    def __init__(self, hierarchy):
        super().__init__(hierarchy)
        self.leaves = set()

    def visit(self, node):
        hierarchy = self.hierarchy

        if not hierarchy.get_children(node):
            self.leaves.add(node)

    def get_leaves(self) -> Set:
        return self.leaves
