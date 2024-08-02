from core.hierarchy.visitor.TopologicalVisitor import TopologicalVisitor


class SubhierarchyBuilderVisitor(TopologicalVisitor):
    def __init__(self, source_hierarchy, roots):
        super().__init__(source_hierarchy)
        from core.hierarchy.Hierarchy import Hierarchy
        self.subhierarchy = Hierarchy(roots)

    def visit(self, node):
        the_hierarchy = super().hierarchy

        for child in the_hierarchy.get_children(node):
            self.subhierarchy.add_edge(child, node)

    def get_result(self):
        return self.subhierarchy
