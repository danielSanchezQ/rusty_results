from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Union, Callable, Generic, Iterator
from patmat_wrappers.option import Option

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')

Result = Union["Ok", "Err"]


class ResultProtocol(ABC, Generic[T, E]):
    @property
    @abstractmethod
    def is_ok(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_err(self) -> bool:
        ...

    @abstractmethod
    def contains(self, value: T) -> bool:
        ...

    @abstractmethod
    def contains_err(self, err: E) -> bool:
        ...

    @abstractmethod
    def ok(self) -> Option:
        ...

    @abstractmethod
    def err(self) -> Option:
        ...

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> Result:
        ...

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        ...

    @abstractmethod
    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        ...

    @abstractmethod
    def map_err(self, f: Callable[[E], U]) -> Result:
        ...

    @abstractmethod
    def iter(self) -> Iterator[T]:
        ...

    @abstractmethod
    def _and(self, res: Result) -> Result:
        ...

    @abstractmethod
    def and_then(self, op: Callable[[T], Result]) -> Result:
        ...

    @abstractmethod
    def _or(self, res: Result) -> Result:
        ...

    @abstractmethod
    def or_else(self, op: Callable[[E], U]) -> Result:
        ...

    @abstractmethod
    def unwrap(self) -> T:
        ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        ...

    @abstractmethod
    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        ...

    @abstractmethod
    def expect(self, msg: str) -> T:
        ...

    @abstractmethod
    def expect_err(self, msg: str) -> E:
        ...

    @abstractmethod
    def unwrap_err(self) -> E:
        ...

    def __and__(self, other: Result) -> Result:
        return self._and(other)

    def __or__(self, other: Result) -> Result:
        return self._or(other)

    def __contains__(self, item: T) -> bool:
        return self.contains(item)

    def __iter__(self) -> Iterator[T]:
        return self.iter()


@dataclass
class Ok(ResultProtocol):
    Vale: T


@dataclass
class Err(Result):
    Error: E
