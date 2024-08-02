# AllPathsToNodeVisitor.py
from core.hierarchy.visitor.TopologicalVisitor import TopologicalVisitor


class AllPathsToNodeVisitor(TopologicalVisitor):
    def __init__(self, hierarchy, end_point):
        super().__init__(hierarchy)
        self.all_paths = []
        self.path_map = {root: [[root]] for root in hierarchy.get_roots()}
        self.end_point = end_point

    def visit(self, node):
        if node in self.hierarchy.get_roots():
            return

        paths_to_node = []
        for parent in self.hierarchy.get_parents(node):
            for path in self.path_map[parent]:
                new_path = path + [node]
                paths_to_node.append(new_path)

        if node == self.end_point:
            self.all_paths = paths_to_node
        else:
            self.path_map[node] = paths_to_node

    def get_all_paths(self):
        return self.all_paths
