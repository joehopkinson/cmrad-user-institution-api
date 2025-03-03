from abc import ABC, abstractmethod
from typing import Optional


class Repository(ABC):
    @abstractmethod
    def get(self, id: str) -> Optional[object]:
        raise NotImplementedError

    @abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError
