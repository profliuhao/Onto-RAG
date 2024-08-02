from typing import Set, HashSet, HashMap, Map, AnyStr, Any, Tuple
from collections import defaultdict


class AreaTaxonomy:
    def __init__(
            self,
            factory: "PAreaTaxonomyFactory",
            hierarchy: "Hierarchy[T]",
            source_hierarchy: "Hierarchy[Concept]",
            derivation: "PAreaTaxonomyDerivation"):

        self.factory = factory
        self.hierarchy = hierarchy
        self.source_hierarchy = source_hierarchy
        self.derivation = derivation

        super().__init__(hierarchy, source_hierarchy, derivation)

    @staticmethod
    def make_derivation(
            factory: "PAreaTaxonomyFactory",
            root: "Concept") -> "SimplePAreaTaxonomyDerivation":

        derivation = SimplePAreaTaxonomyDerivation(root, factory)

        return derivation

    def get_derivation(self) -> "PAreaTaxonomyDerivation":
        return super().get_derivation()

    def get_p_area_taxonomy_factory(self) -> "PAreaTaxonomyFactory":
        return self.factory

    def get_area_hierarchy(self) -> "Hierarchy[T]":
        return super().get_node_hierarchy()

    def get_areas(self) -> "Set[T]":
        return super().get_nodes()

    def search_nodes(self, query: AnyStr) -> "Set[T]":
        return self.find_areas(query)

    def find_areas(self, query: AnyStr) -> "Set[T]":
        query = query.lower()

        search_results = set()

        areas = self.get_areas()

        searched_rels = query.split(", ")

        if not searched_rels:
            return search_results

        for area in areas:
            rels_in_area = []

            for rel in area.get_relationships():
                rels_in_area.append(rel.getName().lower())

            all_rels_found = True

            for rel in searched_rels:
                rel_found = False

                for area_rel in rels_in_area:
                    if area_rel.contains(rel):
                        rel_found = True
                        break

                if not rel_found:
                    all_rels_found = False
                    break

            if all_rels_found:
                search_results.add(area)

        return search_results

    def get_parent_node_details(self, area: "T") -> "Set[ParentNodeDetails[T]]":
        return AbstractionNetworkUtils.get_multi_rooted_node_parent_node_details(
            area,
            self.get_source_hierarchy(),
            self.get_areas())

    def get_properties_in_taxonomy(self) -> "Set[InheritableProperty]":
        properties = set()

        for area in self.get_areas():
            properties.update(area.get_relationships())

        return properties

    def get_concept_areas(self) -> "Map[Concept, Area]":
        concept_areas = {}

        for area in self.get_areas():
            for concept in area.getConcepts():
                concept_areas[concept] = area

        return concept_areas
