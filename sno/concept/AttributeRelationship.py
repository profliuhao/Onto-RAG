class AttributeRelationship:
    def __init__(self, relationship_type, target, relationship_group, characteristic_type):
        self.relationship_type = relationship_type
        self.target = target
        self.relationship_group = relationship_group
        self.characteristic_type = characteristic_type

    def is_defining(self):
        return self.characteristic_type == 900000000000011006 or self.characteristic_type == 900000000000010007

    def get_type(self):
        return self.relationship_type

    def get_target(self):
        return self.target

    def get_group(self):
        return self.relationship_group

    def get_characteristic_type(self):
        return self.characteristic_type

    def __eq__(self, other):
        if isinstance(other, AttributeRelationship):
            return self.equals_ignore_group(other) and (self.get_group() == other.get_group())

        return False

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    def equals_ignore_group(self, other):
        return self.get_type() == other.get_type() and self.get_target() == other.get_target()
