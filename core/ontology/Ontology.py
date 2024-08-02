# Ontology.py

class Ontology:
    def __init__(self, concept_hierarchy):
        self.concept_hierarchy = concept_hierarchy
        self.concepts = {c.get_id(): c for c in concept_hierarchy.get_nodes()}

    def get_concept_hierarchy(self):
        return self.concept_hierarchy

    def get_concept_by_id(self, concept_id):
        return self.concepts.get(concept_id)
