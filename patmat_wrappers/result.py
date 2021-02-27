from abc import ABC, abstractmethod
from hashlib import blake2b
from dataclasses import dataclass
from typing import TypeVar, Union, Callable, Generic, Iterator
from patmat_wrappers.option import Option, Some, Empty
from patmat_wrappers.exceptions import UnwrapException

# base inner type generic
T = TypeVar('T')
# base error type generic
E = TypeVar('E')
# generic callable args for T -> U, E -> U
U = TypeVar('U')


class ResultProtocol(ABC):
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
    def map(self, f: Callable[[T], U]) -> "Result[U, E]":
        ...

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        ...

    @abstractmethod
    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        ...

    @abstractmethod
    def map_err(self, f: Callable[[E], U]) -> "Result[U, E]":
        ...

    @abstractmethod
    def iter(self) -> Iterator[T]:
        ...

    @abstractmethod
    def and_then(self, op: Callable[[T], "Result[T, E]"]) -> "Result[T, E]":
        ...

    @abstractmethod
    def _or(self, res: "Result[T, E]") -> "Result[T, E]":
        ...

    @abstractmethod
    def or_else(self, op: Callable[[E], U]) -> "Result[T, U]":
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

    @abstractmethod
    def __bool__(self) -> bool:
        ...

    def __contains__(self, item: T) -> bool:
        return self.contains(item)

    def __iter__(self) -> Iterator[T]:
        return self.iter()


@dataclass(eq=True, frozen=True)
class Ok(Generic[T], ResultProtocol):
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

    def map(self, f: Callable[[T], U]) -> "Result[T, E]":
        return Ok(f(self.Value))

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self.Value)

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return f(self.Value)

    def map_err(self, f: Callable[[E], U]) -> "Result[T, U]":
        return self

    def iter(self) -> Iterator[T]:
        def _iter():
            yield self.Value
        return iter(_iter())

    def _and(self, res: "Result[T, E]") -> "Result[T, E]":
        return self and res

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return op(self.Value)

    def _or(self, res: "Result[T, E]") -> "Result[T, E]":
        return self or res

    def or_else(self, op: Callable[[E], U]) -> "Result[T, U]":
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

    def __repr__(self):
        return f"Ok({self.Value})"

    def __bool__(self):
        return True


@dataclass(eq=True, frozen=True)
class Err(Generic[E], ResultProtocol):
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

    def map(self, f: Callable[[T], U]) -> "Result[U, E]":
        return self

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return default(self.Error)

    def map_err(self, f: Callable[[E], U]) -> "Result[T, U]":
        return Err(f(self.Error))

    def iter(self) -> Iterator[T]:
        return iter(e for e in tuple())

    def _and(self, res: "Result[T, E]") -> "Result[T, E]":
        return self and res

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return self

    def _or(self, res: "Result[T, E]") -> "Result[T, E]":
        return self or res

    def or_else(self, op: Callable[[E], U]) -> "Result[T, U]":
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

    def __repr__(self):
        return f"Err({self.Error})"

    def __bool__(self):
        return False


Result = Union[Ok[T], Err[E]]
