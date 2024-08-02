# TopologicalVisitor.py
from core.hierarchy.visitor.HierarchyVisitor import HierarchyVisitor


class TopologicalVisitor(HierarchyVisitor):
    def __init__(self, hierarchy):
        super().__init__(hierarchy)
