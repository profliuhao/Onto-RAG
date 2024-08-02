from core.hierarchy.Hierarchy import Hierarchy
from core.ontology.Concept import Concept
from core.abn.node.SinglyRootedNode import SinglyRootedNode
from core.abn.pareataxonomy.InheritableProperty import InheritableProperty
from typing import Set

class PArea(SinglyRootedNode):
    def __init__(self, conceptHierarchy: Hierarchy[Concept], relationships: Set[InheritableProperty]):
        super().__init__(conceptHierarchy)
        self.relationships = relationships

    def equals(self, o: object) -> bool:
        if o is self:
            return True
        if isinstance(o, PArea):
            other: PArea = o
            return super().equals(other) and self.relationships == other.relationships
        return False

    def getRelationships(self) -> Set[InheritableProperty]:
        return self.relationships
