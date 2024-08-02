from typing import Set
from abc import ABC, abstractmethod

from core.ontology.Concept import Concept


class Node(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_concept_count(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_concepts(self) -> Set[Concept]:
        pass

    def __eq__(self, other: object) -> bool:
        return self.__class__ == other.__class__ and self.get_concepts() == other.get_concepts()

    def __hash__(self) -> int:
        return hash(self.get_name())

    def __str__(self) -> str:
        return self.get_name()
