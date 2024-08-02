from collections import deque

from core.hierarchy.Graph import Graph
from core.hierarchy.visitor.AllPathsToNodeVisitor import AllPathsToNodeVisitor
from core.hierarchy.visitor.AncestorHierarchyBuilderVisitor import AncestorHierarchyBuilderVisitor
from core.hierarchy.visitor.HierarchyDepthVisitor import HierarchyDepthVisitor
from core.hierarchy.visitor.LowestCommonAncestorVisitor import LowestCommonAncestorVisitor
from core.hierarchy.visitor.RetrieveLeavesVisitor import RetrieveLeavesVisitor
from core.hierarchy.visitor.SubhierarchyBuilderVisitor import SubhierarchyBuilderVisitor
from core.hierarchy.visitor.SubhierarchyMembersVisitor import SubhierarchyMembersVisitor
from core.hierarchy.visitor.SubhierarchySizeVisitor import SubhierarchySizeVisitor
from core.hierarchy.visitor.TopRootVisitor import TopRootVisitor
from core.hierarchy.visitor.TopologicalListVisitor import TopologicalListVisitor


class Hierarchy:
    def __init__(self, roots, source_hierarchy=None):
        self.base_graph = Graph()
        self.roots = set(roots)

        if source_hierarchy is not None:
            self.initialize_subhierarchy(roots, source_hierarchy)
        else:
            for root in roots:
                self.base_graph.add_node(root)

    def initialize_subhierarchy(self, roots, source_hierarchy):
        self.roots = set(roots)

        for root in roots:
            self.base_graph.add_node(root)

        subhierarchy_builder_visitor = SubhierarchyBuilderVisitor(source_hierarchy, roots)
        source_hierarchy.topological_down_in_subhierarchy(roots, subhierarchy_builder_visitor)

        for edge in subhierarchy_builder_visitor.get_result().get_edges():
            self.add_edge_from_edge(edge)

    def is_singly_rooted(self):
        return len(self.roots) == 1

    def get_roots(self):
        return self.roots

    def get_root(self):
        return next(iter(self.roots))

    def size(self):
        return len(self.base_graph.get_nodes())

    def add_node(self, node):
        self.base_graph.add_node(node)

    def add_edge(self, from_node, to_node):
        self.base_graph.add_edge_by_nodes(from_node, to_node)

    def add_edge_from_edge(self, edge):
        self.add_edge(edge.get_source(), edge.get_target())

    def add_hierarchy(self, hierarchy):
        self.roots.update(hierarchy.roots)
        self.add_all_hierarchical_relationships(hierarchy)

    def add_all_hierarchical_relationships(self, hierarchy):
        other_edges = hierarchy.get_edges()

        for node in hierarchy.get_nodes():
            self.add_node(node)

        for edge in other_edges:
            self.add_edge_from_edge(edge)

    def get_subhierarchy_rooted_at(self, root):
        return Hierarchy(set([root]), self)

    def get_subhierarchy_rooted_at_set(self, roots):
        return Hierarchy(roots, self)

    def get_edges(self):
        return self.base_graph.get_edges()

    def get_nodes(self):
        return self.base_graph.get_nodes()

    def get_children(self, node):
        return self.base_graph.get_incoming_edges(node)

    def get_parents(self, node):
        return self.base_graph.get_outgoing_edges(node)

    def contains(self, node):
        return self.base_graph.contains(node)

    def bfs_down(self, starting_points, visitor):
        queue = deque(starting_points)
        visited = set(starting_points)

        while queue and not visitor.is_finished():
            current_node = queue.popleft()
            visitor.visit(current_node)

            node_children = self.get_children(current_node)

            for child in node_children:
                if child not in visited:
                    queue.append(child)
                    visited.add(child)

    def bfs_up(self, starting_points, visitor):
        queue = deque(starting_points)
        visited = set(starting_points)

        while queue and not visitor.is_finished():
            current_node = queue.popleft()
            visitor.visit(current_node)

            node_parents = self.get_parents(current_node)

            for parent in node_parents:
                if parent not in visited:
                    queue.append(parent)
                    visited.add(parent)

    def topological_down(self, visitor):
        self.topological_down_in_subhierarchy(self.get_roots(), visitor)

    def topological_down_in_subhierarchy(self, starting_points, visitor):
        subhierarchy = self.get_descendants(starting_points)
        subhierarchy.update(starting_points)

        parent_count_in_subhierarchy = {}

        for node in subhierarchy:
            parent_count = sum(1 for parent in self.get_parents(node) if parent in subhierarchy)
            parent_count_in_subhierarchy[node] = parent_count

        queue = deque(starting_points)

        while queue and not visitor.is_finished():
            current_node = queue.popleft()

            visitor.visit(current_node)

            node_children = self.get_children(current_node)

            for child in node_children:
                if parent_count_in_subhierarchy[child] == 1:
                    queue.append(child)
                else:
                    parent_count_in_subhierarchy[child] -= 1

    def topological_up(self, starting_point, visitor):
        self.topological_up_by_set(set([starting_point]), visitor)

    def topological_up_by_set(self, starting_points, visitor):
        subhierarchy_nodes = self.get_ancestors(starting_points)
        subhierarchy_nodes.update(starting_points)

        child_count_in_subhierarchy = {}

        for node in subhierarchy_nodes:
            child_count = sum(1 for child in self.get_children(node) if child in subhierarchy_nodes)
            child_count_in_subhierarchy[node] = child_count

        queue = deque(starting_points)

        while queue and not visitor.is_finished():
            current_node = queue.popleft()
            visitor.visit(current_node)

            node_parents = self.get_parents(current_node)

            for parent in node_parents:
                if child_count_in_subhierarchy[parent] == 1:
                    queue.append(parent)
                else:
                    child_count_in_subhierarchy[parent] -= 1

    def count_descendants(self, node):
        visitor = SubhierarchySizeVisitor(self)
        self.bfs_down({node}, visitor)
        return visitor.get_descendant_count() - 1

    def get_descendants(self, nodes):
        visitor = SubhierarchyMembersVisitor(self)
        self.bfs_down(nodes, visitor)
        members = visitor.get_subhierarchy_members()
        members.difference_update(nodes)
        return members

    def get_member_subhierarchy_roots(self, node):
        visitor = TopRootVisitor(self)
        self.bfs_up({node}, visitor)
        return visitor.get_roots()

    def get_ancestor_hierarchy(self, nodes):

        ancestor_roots = set()

        for node in nodes:
            subhierarchies = self.get_member_subhierarchy_roots(node)

            if not subhierarchies:
                ancestor_roots.add(node)
            else:
                ancestor_roots.update(subhierarchies)

        ancestor_hierarchy_visitor = AncestorHierarchyBuilderVisitor(self, Hierarchy(ancestor_roots))
        self.bfs_up(nodes, ancestor_hierarchy_visitor)
        return ancestor_hierarchy_visitor.get_ancestor_hierarchy()

    def get_ancestors(self, nodes):
        ancestors = self.get_ancestor_hierarchy(nodes).get_nodes()
        ancestors.difference_update(nodes)
        return ancestors

    def get_all_paths_to(self, node):
        ancestor_hierarchy = self.get_ancestor_hierarchy({node})
        visitor = AllPathsToNodeVisitor(self, node)
        ancestor_hierarchy.topological_down(visitor)
        return visitor.get_all_paths()

    def get_topological_ordering(self):
        visitor = TopologicalListVisitor(self)
        self.topological_down(visitor)
        return visitor.get_topological_list()

    def get_descendant_hierarchy_within_distance(self, node, max_distance):
        hierarchy = Hierarchy(set([node]))
        level_processed = 0
        level_queue = deque([node])
        processed = set()

        while level_queue and level_processed < max_distance:
            level_processed += 1
            processed.update(level_queue)
            next_level_queue = deque()

            while level_queue:
                level_node = level_queue.popleft()
                node_children = self.get_children(level_node)

                for child in node_children:
                    if child not in processed:
                        next_level_queue.append(child)

                    hierarchy.add_edge(child, level_node)

            level_queue = next_level_queue

        return hierarchy

    def get_topological_descendant_list_within_distance(self, node, distance):
        hierarchy_within_distance = self.get_descendant_hierarchy_within_distance(node, distance)
        visitor = HierarchyDepthVisitor(hierarchy_within_distance)
        hierarchy_within_distance.topological_down(visitor)
        return visitor.get_result()

    def get_siblings(self, node):
        node_parents = self.get_parents(node)
        siblings = set()

        for parent in node_parents:
            siblings.update(self.get_children(parent))

        siblings.discard(node)
        return siblings

    def get_strict_siblings(self, node):
        node_parents = self.get_parents(node)
        strict_siblings = set()

        for parent in node_parents:
            siblings = self.get_children(parent)

            for sibling in siblings:
                if sibling != node and self.get_parents(sibling) == node_parents:
                    strict_siblings.add(sibling)

        strict_siblings.discard(node)
        return strict_siblings

    def get_leaves(self):
        leaves_visitor = RetrieveLeavesVisitor(self)
        self.bfs_down(self.get_roots(), leaves_visitor)
        return leaves_visitor.get_leaves()

    def get_internal_nodes(self):
        leaves = self.get_leaves()
        internal_nodes = self.get_nodes()
        internal_nodes.difference_update(leaves)
        return internal_nodes

    def get_all_longest_path_depths(self):
        hierarchy_depth_visitor = HierarchyDepthVisitor(self)
        self.topological_down(hierarchy_depth_visitor)
        return hierarchy_depth_visitor.get_all_depths()

    def lowest_common_ancestors(self, nodes):
        ancestor_hierarchy = self.get_ancestor_hierarchy(nodes)
        visitor = LowestCommonAncestorVisitor(ancestor_hierarchy, nodes)
        ancestor_hierarchy.topological_up_by_set(nodes, visitor)
        return visitor.get_lowest_common_ancestors()

    def is_ancestor_of(self, potential_ancestor, node):

        return potential_ancestor in self.get_ancestors({node})

    def is_descendant_of(self, potential_descendant, node):
        return potential_descendant in self.get_descendants({node})
