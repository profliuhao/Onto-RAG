
from collections import defaultdict

from core.ontology.Ontology import Ontology



class SCTRelease(Ontology):
    class DescriptionEntry:
        def __init__(self, description, concept):
            self.description = description
            self.concept = concept

    def __init__(self, release_info, active_concept_hierarchy, all_concepts):
        super().__init__(active_concept_hierarchy)
        self.release_info = release_info
        self.descriptions = []
        self.subhierarchies_with_attribute_rels = set()

        for root in active_concept_hierarchy.get_children(active_concept_hierarchy.get_root()):
            hierarchy = active_concept_hierarchy.get_subhierarchy_rooted_at(root)
            if any(p for p in hierarchy.get_nodes() if len(p.get_attribute_relationships()) != 0):
                self.subhierarchies_with_attribute_rels.add(root)

        self.attribute_relationship_types = active_concept_hierarchy.get_subhierarchy_rooted_at(
            self.get_concept_from_id(410662002)).get_nodes()

        concepts = {concept.get_id(): concept for concept in all_concepts}

        for concept in all_concepts:
            for description in concept.get_descriptions():
                self.descriptions.append(self.DescriptionEntry(description, concept))

        self.descriptions.sort(key=lambda x: x.description.get_term().lower())
        self.starting_index = self._generate_starting_index(self.descriptions)

    def get_release_info(self):
        return self.release_info

    def get_hierarchies_with_attribute_relationships(self):
        return self.subhierarchies_with_attribute_rels

    def get_available_attribute_relationships(self):
        return self.attribute_relationship_types

    def get_concept_hierarchy(self):
        return super().get_concept_hierarchy()

    def get_concept_from_id(self, concept_id):
        return self.concepts.get(concept_id)

    def get_all_concepts(self):
        return set(self.concepts.values())

    def get_active_concepts(self):
        return {concept for concept in self.concepts.values() if concept.is_active()}

    def get_inactive_concepts(self):
        return {concept for concept in self.concepts.values() if not concept.is_active()}

    def get_primitive_concepts(self):
        return {concept for concept in self.concepts.values() if concept.is_primitive()}

    def get_fully_defined_concepts(self):
        return {concept for concept in self.concepts.values() if not concept.is_primitive()}

    def search_exact(self, term):
        term = term.lower()
        if len(term) < 3:
            return set()

        first_char = term[0].lower()
        results = set()
        start_index = self._get_start_index(first_char)

        for entry in self.descriptions[start_index:]:
            desc_first_char = entry.description.get_term()[0].lower()
            if desc_first_char == first_char:
                if entry.description.get_term().lower() == term and entry.concept.is_active():
                    results.add(entry.concept)
            else:
                break

        return results

    def search_starting(self, term):
        term = term.lower()
        if len(term) < 3:
            return set()

        first_char = term[0].lower()
        results = set()
        start_index = self._get_start_index(first_char)

        for entry in self.descriptions[start_index:]:
            desc_first_char = entry.description.get_term()[0].lower()
            if desc_first_char == first_char:
                if entry.description.get_term().lower().startswith(term) and entry.concept.is_active():
                    results.add(entry.concept)
            else:
                break

        return results

    def search_anywhere(self, term):
        term = term.lower()
        results = set()
        for entry in self.descriptions:
            if term in entry.description.get_term().lower() and entry.concept.is_active():
                results.add(entry.concept)

        return results

    def search_id(self, query):
        results = set()
        try:
            concept_id = int(query)
            if concept_id in self.concepts:
                results.add(self.concepts[concept_id])
        except ValueError:
            pass

        return results

    def supports_stated_relationships(self):
        return False

    def _get_start_index(self, first_char):
        if first_char < 'a':
            return 0
        elif first_char > 'z':
            return self.starting_index['z']
        else:
            return self.starting_index[first_char]

    def _generate_starting_index(self, descriptions):
        starting_index = defaultdict(int)
        last_char = descriptions[0].description.get_term()[0].lower()

        for c in range(1, len(descriptions)):
            term = descriptions[c].description.get_term()
            cur_char = term[0].lower()

            if cur_char != last_char:
                if 'a' <= cur_char <= 'z':
                    starting_index[cur_char] = c

                last_char = cur_char

        return starting_index
