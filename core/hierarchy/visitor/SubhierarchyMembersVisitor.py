from typing import Set

from core.hierarchy.visitor.HierarchyVisitor import HierarchyVisitor


class SubhierarchyMembersVisitor(HierarchyVisitor):
    def __init__(self, the_hierarchy):
        super().__init__(the_hierarchy)
        self.members = set()

    def visit(self, node):
        self.members.add(node)

    def get_subhierarchy_members(self) -> Set:
        return self.members
