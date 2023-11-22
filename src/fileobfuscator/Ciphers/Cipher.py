from abc import ABC, abstractmethod


class Cipher(ABC):
    @staticmethod
    @abstractmethod
    def encode(string: str) -> str:
        ...

    @staticmethod
    @abstractmethod
    def decode(string: str) -> str:
        ...

