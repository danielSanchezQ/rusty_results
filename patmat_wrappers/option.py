from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Union, Callable

T = TypeVar('T')

Option = Union["Some", "Empty"]


class OptionProtocol(ABC):
    @property
    @abstractmethod
    def is_some(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        ...

    @abstractmethod
    def contains(self, item: T) -> bool:
        ...

    @abstractmethod
    def expects(self, msg: str) -> T:
        ...

    @abstractmethod
    def unwrap(self) -> T:
        ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        ...

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[], T]):
        ...

    @abstractmethod
    def map(self, f: Callable[[T], T]) -> "Option":
        ...

    @abstractmethod
    def map_or(self, default: T, f: Callable[[T], T]) -> Option:
        ...

    @abstractmethod
    def map_or_else(self, default: Callable[[], T], f: Callable[[T], T]) -> Option:
        ...

    @abstractmethod
    def ok_or(self, err: Exception) -> "Result":
        ...

    @abstractmethod
    def ok_or_else(self, f: Callable[[], Exception]) -> "Result":
        ...

    def __contains__(self, item: T) -> bool:
        return self.contains(item)


@dataclass
class Some(OptionProtocol):
    Value: T


@dataclass
class Empty(OptionProtocol):
    ...





if __name__ == "__main__":
    print("Compiling")