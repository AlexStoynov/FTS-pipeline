from abc import ABC, abstractmethod

from models.transaction import Transaction


class BaseNormalizer(ABC):
    @abstractmethod
    def normalize(self, file_path: str) -> list[Transaction]:
        ...

