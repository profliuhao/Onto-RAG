# AncestorHierarchyBuilderVisitor.py
from core.hierarchy.visitor.HierarchyVisitor import HierarchyVisitor


class AncestorHierarchyBuilderVisitor(HierarchyVisitor):
    def __init__(self, hierarchy, ancestor_hierarchy):
        super().__init__(hierarchy)
        self.ancestor_hierarchy = ancestor_hierarchy

    def visit(self, node):
        for parent in self.hierarchy.get_parents(node):
            self.ancestor_hierarchy.add_edge(node, parent)

    def get_ancestor_hierarchy(self):
        return self.ancestor_hierarchy
