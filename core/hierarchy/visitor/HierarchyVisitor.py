# HierarchyVisitor.py

from abc import ABC, abstractmethod

class HierarchyVisitor(ABC):
    def __init__(self, the_hierarchy):
        self._hierarchy = the_hierarchy
        self.finished = False

    @property
    def hierarchy(self):
        return self._hierarchy

    @hierarchy.setter
    def hierarchy(self, value):
        self._hierarchy = value

    @abstractmethod
    def visit(self, node):
        pass

    def is_finished(self):
        return self.finished
