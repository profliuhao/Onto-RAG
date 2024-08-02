from typing import Set

from core.abn.node.Node import Node
from core.hierarchy.Hierarchy import Hierarchy
from core.ontology.Concept import Concept


class MultiRootedNode(Node):
    def __init__(self, hierarchy: 'Hierarchy[Concept]'):
        self.hierarchy = hierarchy

    def get_hierarchy(self) -> 'Hierarchy[Concept]':
        return self.hierarchy

    def get_roots(self) -> Set['Concept']:
        return self.hierarchy.get_roots()
