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
        assert self.Value is not None, msg
        return self.Value

    def unwrap(self) -> T:
        assert self.Value is not None
        return self.Value

    def unwrap_or(self, default: T) -> T:
        return self.Value or default

    def unwrap_or_else(self, f: Callable[[], T]):
        return self.Value or f()

    def map(self, f: Callable[[T], T]) -> "Option":
        return f(self.Value)

    def map_or(self, default: T, f: Callable[[T], T]) -> Option:
        return f(self.Value) or default

    def map_or_else(self, default: Callable[[], T], f: Callable[[T], T]) -> Option:
        return f(self.Value) or default()

    def iter(self) -> Iterator[T]:
        return iter(self.Value)

    def filter(self, predicate: Callable[[T], bool]) -> Option:
        if self.Value is None:
            return None

        return True if predicate(self.Value) else None

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

    def unwrap_or_else(self, f: Callable[[], T]):
        return f()

    def map(self, f: Callable[[T], T]) -> "Option":
        return None

    def map_or(self, default: T, f: Callable[[T], T]) -> Option:
        return default

    def map_or_else(self, default: Callable[[], T], f: Callable[[T], T]) -> Option:
        return default()

    def iter(self) -> Iterator[T]:
        return None

    def filter(self, predicate: Callable[[T], bool]) -> Option:
        return None

