from typing import Set, Dict, Generic, TypeVar
from core.abn.node.MultiRootedNode import MultiRootedNode
from core.abn.node.SinglyRootedNode import SinglyRootedNode
from abc import abstractmethod

from core.hierarchy.Hierarchy import Hierarchy

T = TypeVar('T', bound=SinglyRootedNode)

class PartitionedNode(Generic[T], MultiRootedNode):
    def __init__(self, internal_nodes: Set[T]):
        super().__init__(PartitionedNode.create_internal_hierarchy(internal_nodes))
        self.internal_nodes = internal_nodes
        self.concept_nodes = {}
        for node in self.internal_nodes:
            for concept in node.get_concepts():
                if concept not in self.concept_nodes:
                    self.concept_nodes[concept] = set()
                self.concept_nodes[concept].add(node)

    @staticmethod
    def create_internal_hierarchy(nodes: Set[T]) -> 'Hierarchy[Concept]':
        roots = set(node.get_root() for node in nodes)
        hierarchy = Hierarchy(roots)
        for node in nodes:
            hierarchy.add_all_hierarchical_relationships(node.get_hierarchy())
        return hierarchy

    def get_internal_nodes(self) -> Set[T]:
        return self.internal_nodes

    def get_concepts(self) -> Set['Concept']:
        return set(self.concept_nodes.keys())

    def get_concept_count(self) -> int:
        return len(self.concept_nodes)

    def get_concept_nodes(self) -> 'Dict[Concept, Set[T]]':
        return self.concept_nodes

    def has_overlapping_concepts(self) -> bool:
        processed_concepts = set()
        for node in self.get_internal_nodes():
            for concept in node.get_concepts():
                if concept in processed_concepts:
                    return True
                processed_concepts.add(concept)
        return False

    def get_overlapping_concepts(self) -> Set['Concept']:
        return set(detail.concept for detail in self.get_overlapping_concept_details())

    def get_overlapping_concept_details(self) -> Set['OverlappingConceptDetails[T]']:
        overlapping_results = set()
        for concept, overlapping_nodes in self.get_concept_nodes().items():
            if len(overlapping_nodes) > 1:
                overlapping_results.add(OverlappingConceptDetails(concept, overlapping_nodes))
        return overlapping_results

    @abstractmethod
    def get_name(self, separator: str) -> str:
        pass


class OverlappingConceptDetails(Generic[T]):
    def __init__(self, concept: 'Concept', overlapping_nodes: Set[T]):
        self.concept = concept
        self.overlapping_nodes = overlapping_nodes

    def get_concept(self) -> 'Concept':
        return self.concept

    def get_overlapping_nodes(self) -> Set[T]:
        return self.overlapping_nodes
