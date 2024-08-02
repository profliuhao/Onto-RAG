from typing import Set, TypeVar

from core.abn.pareataxonomy.AreaTaxonomy import AreaTaxonomy
from core.hierarchy.Hierarchy import Hierarchy

Area = TypeVar('Area')
PArea = TypeVar('PArea')
T = TypeVar('T')

class PAreaTaxonomy(PartitionedAbstractionNetwork[T, Area]):
    def __init__(self, area_taxonomy: AreaTaxonomy, parea_hierarchy: Hierarchy[T], concept_hierarchy: Hierarchy[Concept], derivation: PAreaTaxonomyDerivation):
        super().__init__(area_taxonomy, parea_hierarchy, concept_hierarchy, derivation)

    # def __init__(self, area_taxonomy: AreaTaxonomy, parea_hierarchy: Hierarchy[T], concept_hierarchy: Hierarchy[Concept]):
    #     super().__init__(area_taxonomy, parea_hierarchy, concept_hierarchy, SimplePAreaTaxonomyDerivation(concept_hierarchy.get_root(), area_taxonomy.get_parea_taxonomy_factory()))
    #
    # def __init__(self, taxonomy: 'PAreaTaxonomy'):
    #     self.__init__(taxonomy.get_area_taxonomy(), taxonomy.get_parea_hierarchy(), taxonomy.get_source_hierarchy(), taxonomy.get_derivation())
    #
    # def __init__(self, taxonomy: 'PAreaTaxonomy', derivation: PAreaTaxonomyDerivation):
    #     self.__init__(taxonomy.get_area_taxonomy(), taxonomy.get_parea_hierarchy(), taxonomy.get_source_hierarchy(), derivation)

    def get_derivation(self) -> PAreaTaxonomyDerivation:
        return super().get_derivation()

    def get_cached_derivation(self) -> CachedAbNDerivation[PAreaTaxonomy]:
        return super().get_cached_derivation()

    def get_parea_taxonomy_factory(self) -> PAreaTaxonomyFactory:
        return super().get_area_taxonomy().get_parea_taxonomy_factory()

    def get_area_taxonomy(self) -> AreaTaxonomy:
        return super().get_base_abstraction_network()

    def get_parea_hierarchy(self) -> Hierarchy[T]:
        return super().get_node_hierarchy()

    def get_area_for(self, parea: T) -> Area:
        return super().get_partition_node_for(parea)

    def get_root_parea(self) -> T:
        return self.get_parea_hierarchy().get_root()

    def get_areas(self) -> Set[Area]:
        return super().get_areas()

    def get_pareas(self) -> Set[T]:
        return super().get_nodes()

    def get_parent_node_details(self, parea: T) -> Set[ParentNodeDetails[T]]:
        return AbstractionNetworkUtils.get_singly_rooted_node_parent_node_details(parea, self.get_source_hierarchy(), self.get_pareas())

    def create_root_subtaxonomy(self, root: T) -> 'PAreaTaxonomy':
        subhierarchy = self.get_parea_hierarchy().get_subhierarchy_rooted_at(root)
        generator = PAreaTaxonomyGenerator()
        subtaxonomy = generator.create_taxonomy_from_pareas(self.get_parea_taxonomy_factory(), subhierarchy, self.get_source_hierarchy())
        root_subtaxonomy = RootSubtaxonomy(self, subtaxonomy)
        return root_subtaxonomy

    def create_ancestor_subtaxonomy(self, source: T) -> 'PAreaTaxonomy':
        subhierarchy = self.get_parea_hierarchy().get_ancestor_hierarchy(source)
        generator = PAreaTaxonomyGenerator()
        ancestor_subtaxonomy = generator.create_taxonomy_from_pareas(self.get_parea_taxonomy_factory(), subhierarchy,
                                                                     self.get_source_hierarchy())
        return AncestorSubtaxonomy(self, source, ancestor_subtaxonomy)

    def is_aggregated(self) -> bool:
        return False

    def get_properties_in_taxonomy(self) -> Set:
        return self.get_area_taxonomy().get_properties_in_taxonomy()

    def get_relationship_subtaxonomy(self, allowed_rel_types: Set) -> 'PAreaTaxonomy':
        if allowed_rel_types == self.get_properties_in_taxonomy():
            return self
        else:
            generator = PAreaTaxonomyGenerator()
            factory = PAreaRelationshipSubtaxonomyFactory(self.get_parea_taxonomy_factory().get_source_ontology(), self,
                                                          allowed_rel_types)
            return generator.derive_parea_taxonomy(factory, self.get_source_hierarchy())

    def get_aggregated(self, ap) -> 'PAreaTaxonomy':
        return AggregatePAreaTaxonomy.generate_aggregate_parea_taxonomy(self, ap)
