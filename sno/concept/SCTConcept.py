from core.ontology.Concept import Concept


class SCTConcept(Concept):
    UNSET_FSN = "FSN_NOT_SET"

    def __init__(self, _id, is_primitive, is_active):
        super().__init__(_id)
        self.is_primitive = is_primitive
        self.is_active = is_active
        self.desc_list = set()
        self.lateral_relationships = set()
        self.fully_specified_name = SCTConcept.UNSET_FSN

    def is_primitive(self):
        return self.is_primitive

    def is_active(self):
        return self.is_active

    def set_lateral_relationships(self, rels):
        self.lateral_relationships.clear()
        self.lateral_relationships.update(rels)

    def set_descriptions(self, descriptions):
        self.desc_list.clear()
        self.desc_list.update(descriptions)

        for d in self.desc_list:
            if d.get_description_type() == 3:
                fsn = d.get_term().split(" (")[0] if " (" in d.get_term() else d.get_term()
                self.fully_specified_name = fsn
                break

    def get_attribute_relationships(self):
        return self.lateral_relationships

    def get_descriptions(self):
        return self.desc_list

    def get_name(self):
        return self.fully_specified_name

    def get_id_as_string(self):
        return str(self.get_id())

    def __eq__(self, other):
        if isinstance(other, SCTConcept):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
