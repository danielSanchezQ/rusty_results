from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Union, Callable, Generic, Iterator
from patmat_wrappers.option import Option, Some, Empty
from patmat_wrappers.exceptions import UnwrapException

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
    def unwrap_err(self) -> E:
        ...

    @abstractmethod
    def expect_err(self, msg: str) -> E:
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
    Value: T

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False

    def contains(self, value: T) -> bool:
        return self.Value == value

    def contains_err(self, err: E) -> bool:
        return False

    def ok(self) -> Option:
        return Some(self.Value)

    def err(self) -> Option:
        return Empty()

    def map(self, f: Callable[[T], U]) -> Result:
        return Ok(f(self.Value))

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return self.map(f)

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return self.map(f)

    def map_err(self, f: Callable[[E], U]) -> Result:
        return self

    def iter(self) -> Iterator[T]:
        def _iter():
            yield self.Value
        return iter(_iter())

    def _and(self, res: Result) -> Result:
        return res

    def and_then(self, op: Callable[[T], Result]) -> Result:
        return op(self.Value)

    def _or(self, res: Result) -> Result:
        return self

    def or_else(self, op: Callable[[E], U]) -> Result:
        return self

    def unwrap(self) -> T:
        return self.Value

    def unwrap_or(self, default: T) -> T:
        return self.Value

    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        return self.Value

    def expect(self, msg: str) -> T:
        return self.Value

    def unwrap_err(self) -> E:
        raise UnwrapException(f"{self.Value}")

    def expect_err(self, msg: str) -> E:
        raise UnwrapException(msg)


@dataclass
class Err(ResultProtocol):
    Error: E

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True

    def contains(self, value: T) -> bool:
        return False

    def contains_err(self, err: E) -> bool:
        return self.Error == err

    def ok(self) -> Option:
        return Empty()

    def err(self) -> Option:
        return Some(self.Error)

    def map(self, f: Callable[[T], U]) -> Result:
        return self

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return default(self.Error)

    def map_err(self, f: Callable[[E], U]) -> Result:
        return Err(f(self.Error))

    def iter(self) -> Iterator[T]:
        return iter(e for e in tuple())

    def _and(self, res: Result) -> Result:
        return self

    def and_then(self, op: Callable[[T], Result]) -> Result:
        return self

    def _or(self, res: Result) -> Result:
        return res

    def or_else(self, op: Callable[[E], U]) -> Result:
        return Err(op(self.Error))

    def unwrap(self) -> T:
        raise UnwrapException(self.Error)

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        return default()

    def expect(self, msg: str) -> T:
        raise UnwrapException(msg)

    def unwrap_err(self) -> E:
        return self.Error

    def expect_err(self, msg: str) -> E:
        return self.Error
