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

    @abstractmethod
    def _or(self, optb: Option) -> Option:
        ...

    @abstractmethod
    def or_else(self, f: Callable[[T], Option]) -> Option:
        ...

    @abstractmethod
    def xor(self, optb: Option) -> Option:
        ...

    def __and__(self, other: Option) -> Option:
        return self._and(other)

    def __or__(self, other: Option) -> Option:
        return self._or(other)

    def __contains__(self, item: T) -> bool:
        return self.contains(item)

    def __iter__(self):
        return self.iter()

"""
pub fn get_or_insert(&mut self, value: T) -> &mut Tⓘ
pub fn get_or_insert_with<F>(&mut self, f: F) -> &mut Tⓘ
pub fn take(&mut self) -> Option<T>
pub fn replace(&mut self, value: T) -> Option<T>
pub fn zip<U>(self, other: Option<U>) -> Option<(T, U)>
pub fn zip_with<U, F, R>(self, other: Option<U>, f: F) -> Option<R>
pub fn copied(self) -> Option<T>
pub fn copied(self) -> Option<T>
pub fn cloned(self) -> Option<T>
pub fn cloned(self) -> Option<T>
pub fn expect_none(self, msg: &str)
pub fn unwrap_none(self)
pub fn unwrap_or_default(self) -> T
pub fn as_deref(&self) -> Option<&<T as Deref>::Target>
pub fn as_deref_mut(&mut self) -> Option<&mut <T as Deref>::Target>
pub fn transpose(self) -> Result<Option<T>, E>
pub fn flatten(self) -> Option<T>
"""


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

    def _or(self, optb: Option) -> Option:
        return Some(self.Value)

    def or_else(self, f: Callable[[T], Option]) -> Option:
        return Some(self.Value)

    def xor(self, optb: Option) -> Option:
        """
        Returns Some if exactly one of self, optb is Some, otherwise returns None.
        Tengo dudas con este por eso pongo el comentario
        """
        return Some(self.Value)


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

    def _or(self, optb: Option) -> Option:
        return optb

    def or_else(self, f: Callable[[T], Option]) -> Option:
        return f()

    def xor(self, optb: Option) -> Option:
        """
        Returns Some if exactly one of self, optb is Some, otherwise returns None.
        Tengo dudas con este por eso pongo el comentario
        """
        return Empty
