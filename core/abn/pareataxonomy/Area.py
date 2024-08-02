import hashlib

from typing import List, Set


class Area:
    def __init__(self, pareas: Set['PArea'], relationships: Set['InheritableProperty']):
        self.pareas = pareas
        self.relationships = relationships
        self.regions = set()

        region_partition = {}

        for parea in pareas:
            parea_relationships = frozenset(parea.get_relationships())
            matched_region = region_partition.get(parea_relationships)

            if matched_region is not None:
                region_partition[parea_relationships].add(parea)
            else:
                region_partition[parea_relationships] = set()
                region_partition[parea_relationships].add(parea)

        for rels, region_pareas in region_partition.items():
            self.regions.add(Region(self, region_pareas, rels))

    def get_relationships(self) -> Set['InheritableProperty']:
        return self.relationships

    def get_regions(self) -> Set['Region']:
        return self.regions

    def get_pareas(self) -> Set['PArea']:
        return self.pareas

    def get_name(self) -> str:
        return self.getName(", ")

    def get_name(self, separator: str) -> str:
        if not self.relationships:
            return "∅"  # Empty set symbol
        else:
            rel_names = [rel.getName() for rel in self.relationships]
            rel_names.sort()
            return separator.join(rel_names)

    def hash_code(self) -> int:
        return hash(self.relationships)

    def equals(self, o: object) -> bool:
        if isinstance(o, Area):
            other_area = o
            return self.get_relationships() == other_area.get_relationships()
        return False
