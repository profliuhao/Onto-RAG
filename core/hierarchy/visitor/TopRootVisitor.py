# TopRootVisitor.py

from typing import Set

from core.hierarchy.visitor.HierarchyVisitor import HierarchyVisitor


class TopRootVisitor(HierarchyVisitor):
    def __init__(self, the_hierarchy):
        super().__init__(the_hierarchy)
        self.roots = set()

    def visit(self, node):
        the_hierarchy = super().hierarchy

        if node in the_hierarchy.get_roots():
            self.roots.add(node)

    def get_roots(self):
        return self.roots

