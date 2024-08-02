from typing import Set, Dict, Generic, TypeVar

from SinglyRootedNode import SinglyRootedNode

T = TypeVar('T', bound=SinglyRootedNode)

class OverlappingConceptDetails(Generic[T]):
    def __init__(self, concept: 'Concept', overlapping_nodes: Set[T]):
        self.concept = concept
        self.overlapping_nodes = overlapping_nodes

    def get_concept(self) -> 'Concept':
        return self.concept

    def get_overlapping_nodes(self) -> Set[T]:
        return self.overlapping_nodes
