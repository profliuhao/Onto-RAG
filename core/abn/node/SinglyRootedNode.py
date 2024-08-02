from abc import ABC
from typing import Set

from core.abn.node.Node import Node
from core.hierarchy.Hierarchy import Hierarchy
from core.ontology.Concept import Concept


class SinglyRootedNode(Node, ABC):
    def __init__(self, hierarchy: Hierarchy):
        self.hierarchy = hierarchy

    def get_hierarchy(self) -> Hierarchy:
        return self.hierarchy

    def get_root(self) -> Concept:
        return self.hierarchy.get_root()

    def get_concepts(self) -> Set[Concept]:
        return self.hierarchy.get_nodes()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SinglyRootedNode):
            other_node = other.get_root()
            return self.get_root().equals(other_node)
        return False

    def __hash__(self) -> int:
        return self.get_root().hash_code()

    def get_concept_count(self) -> int:
        return self.hierarchy.size()

    def get_name(self) -> str:
        return f"{self.get_root().getName()}"
