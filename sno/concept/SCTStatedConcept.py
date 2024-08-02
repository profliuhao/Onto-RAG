from sno.concept.SCTConcept import SCTConcept


class SCTStatedConcept(SCTConcept):
    def __init__(self, _id, is_primitive, is_active):
        super().__init__(_id, is_primitive, is_active)
        self.stated_attribute_relationships = set()

    def set_stated_relationships(self, stated_attribute_relationships):
        self.stated_attribute_relationships.clear()
        self.stated_attribute_relationships.update(stated_attribute_relationships)

    def get_stated_relationships(self):
        return self.stated_attribute_relationships

    def __eq__(self, other):
        if isinstance(other, SCTStatedConcept):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
