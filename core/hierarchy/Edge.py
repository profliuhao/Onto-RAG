# Edge.py

class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

    def get_source(self):
        return self.from_node

    def get_target(self):
        return self.to_node

    def __eq__(self, other):
        if isinstance(other, Edge):
            return other.from_node == self.from_node and other.to_node == self.to_node
        return False

    def __hash__(self):
        return hash(self.from_node) + hash(self.to_node)

