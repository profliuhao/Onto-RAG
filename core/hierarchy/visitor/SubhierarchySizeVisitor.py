# SubhierarchySizeVisitor.py
from core.hierarchy.visitor.HierarchyVisitor import HierarchyVisitor


class SubhierarchySizeVisitor(HierarchyVisitor):
    def __init__(self, hierarchy):
        super().__init__(hierarchy)
        self.count = 0

    def visit(self, node):
        self.count += 1

    def get_descendant_count(self):
        return self.count
