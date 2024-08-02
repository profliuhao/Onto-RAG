# Concept.py

class Concept:
    def __init__(self, concept_id):
        self.id = concept_id

    def get_id(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, Concept):
            return self.id == other.id
        return False

    def equals(self, other):
        if isinstance(other, Concept):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def hash_code(self):
        return hash(self.id)
