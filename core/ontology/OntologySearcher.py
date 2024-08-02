from abc import ABC, abstractmethod
from typing import Set


class OntologySearcher(ABC):

    @abstractmethod
    def search_starting(self, term) -> Set:
        pass

    @abstractmethod
    def search_exact(self, term) -> Set:
        pass

    @abstractmethod
    def search_anywhere(self, term) -> Set:
        pass

    @abstractmethod
    def search_id(self, query) -> Set:
        pass
