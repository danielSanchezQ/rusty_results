from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Union, Callable, Iterator


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
    def unwrap_or_else(self, f: Callable[[], T]) -> Option:
        ...

    @abstractmethod
    def map(self, f: Callable[[T], T]) -> Option:
        ...

    @abstractmethod
    def map_or(self, default: T, f: Callable[[T], T]) -> Option:
        ...

    @abstractmethod
    def map_or_else(self, default: Callable[[], T], f: Callable[[T], T]) -> Option:
        ...

    @abstractmethod
    def iter(self) -> Iterator[T]:
        ...

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> Option:
        ...

    @abstractmethod
    def ok_or(self, err: Exception) -> "Result":
        ...

    @abstractmethod
    def ok_or_else(self, f: Callable[[], Exception]) -> "Result":
        ...

    @abstractmethod
    def _and(self, optb: Option) -> Option:
        ...

    @abstractmethod
    def and_then(self, f: Callable[[T], Option]) -> Option:
        ...

    def __and__(self, other: Option) -> Option:
        return self._and(other)

    def __contains__(self, item: T) -> bool:
        return self.contains(item)

    def __iter__(self):
        return self.iter()


@dataclass
class Some(OptionProtocol):
    Value: T

    @property
    def is_some(self) -> bool:
        return True

    @property
    def is_empty(self) -> bool:
        return False

    def contains(self, item: T) -> bool:
        return item == self.Value

    def expects(self, msg: str) -> T:
        return self.Value

    def unwrap(self) -> T:
        return self.Value

    def unwrap_or(self, default: T) -> T:
        return self.Value

    def unwrap_or_else(self, f: Callable[[], T]):
        return self.copy()

    def map(self, f: Callable[[T], T]) -> Option:
        return Some(f(self.Value))

    def map_or(self, default: T, f: Callable[[T], T]) -> Option:
        return Some(f(self.Value))

    def map_or_else(self, default: Callable[[], T], f: Callable[[T], T]) -> Option:
        return Some(f(self.Value))

    def iter(self) -> Iterator[T]:
        return iter(self.Value)

    def filter(self, predicate: Callable[[T], bool]) -> Option:
        return self.copy() if predicate(self.Value) else Empty

    def _and(self, optb: Option) -> Option:
        return optb

    def and_then(self, f: Callable[[T], Option]) -> Option:
        return f(self.Value)

@dataclass
class Empty(OptionProtocol):
    @property
    def is_some(self) -> bool:
        return False

    @property
    def is_empty(self) -> bool:
        return True

    def contains(self, item: T) -> bool:
        return False

    def expects(self, msg: str) -> T:
        assert False, msg

    def unwrap(self) -> T:
        assert False

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, f: Callable[[], T]) -> Option:
        return Some(f())

    def map(self, f: Callable[[T], T]) -> Option:
        return self

    def map_or(self, default: T, f: Callable[[T], T]) -> Option:
        return Some(default)

    def map_or_else(self, default: Callable[[], T], f: Callable[[T], T]) -> Option:
        return Some(default())

    def iter(self) -> Iterator[T]:
        return iter([])

    def filter(self, predicate: Callable[[T], bool]) -> Option:
        return self

    def _and(self, optb: Option) -> Option:
        return Empty

    def and_then(self, f: Callable[[T], Option]) -> Option:
        return Empty

