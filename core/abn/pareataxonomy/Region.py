from typing import Set

from core.abn.node import SimilarityNode
from core.abn.pareataxonomy import InheritableProperty, InheritanceType, PArea
from core.abn.pareataxonomy.Area import Area


class Region(SimilarityNode[PArea]):
    def __init__(self, area: Area, pareas: Set[PArea], relationships: Set[InheritableProperty]):
        super().__init__(pareas)
        self.area = area
        self.relationships = relationships

    def getArea(self) -> Area:
        return self.area

    def getRelationships(self) -> Set[InheritableProperty]:
        return self.relationships

    def getPAreas(self) -> Set[PArea]:
        return super().getInternalNodes()

    def isPAreaInRegion(self, parea: PArea) -> bool:
        return self.getPAreas().contains(parea)

    def hashCode(self) -> int:
        return self.relationships.hashCode()

    def __eq__(self, other):
        if isinstance(other, Region):
            other = Region(other)
            return all(rel.equals_including_inheritance(other.relationships) for rel in self.relationships)
        return False

    def getName(self) -> str:
        return self.getName(", ")

    def getName(self, separator):

        if not self.relationships:
            return "∅"  # Empty set symbol
        else:
            rel_names_and_inheritance = []

            self.getRelationships().forEach(lambda rel: rel_names_and_inheritance.add(rel.getName() + ("+" if rel.getInheritanceType() == InheritanceType.Introduced else "*")))

            rel_names_and_inheritance.sort()

            name = rel_names_and_inheritance[0]

            for c in range(1, len(rel_names_and_inheritance)):
                name += separator
                name += rel_names_and_inheritance[c]

            return name
