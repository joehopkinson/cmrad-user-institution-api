from abc import ABC, abstractmethod
from typing import Any, Optional


class Repository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    def add(self, entity: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: str, data: Any) -> Optional[Any]:
        raise NotImplementedError
