from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Union, Callable, Generic, Iterator, Tuple
from rusty_results.exceptions import UnwrapException

# base inner type generic
T = TypeVar('T')
# base error type generic
E = TypeVar('E')
# generic callable args for T -> U, E -> U
U = TypeVar('U')
R = TypeVar('R')


class OptionProtocol(Generic[T]):
    @property
    @abstractmethod
    def is_some(self) -> bool:
        """
        :return: True if the option is `Some`.
        """
        ...

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """
        :return: True if the option is `Empty`.
        """
        ...

    @abstractmethod
    def contains(self, item: T) -> bool:
        """
        :param item: The value to check.
        :return: True if the option is `Some` containing the given value.
        """
        ...

    @abstractmethod
    def expects(self, msg: str) -> T:
        """
        :param msg: Attached message for `UnwrapException` if raised.
        :return: The contained `Some` value
        :raises: `UnwrapException` if option is Empty.
        """
        ...

    @abstractmethod
    def unwrap(self) -> T:
        """
        Because this function may panic, its use is generally discouraged.
        Instead, prefer to use pattern matching and handle the None case explicitly, or call unwrap_or, unwrap_or_else,
        or unwrap_or_default

        :return: The contained Some value, consuming the self value.
        :raises: `UnwrapException` if option is `Empty`
        """
        ...

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """
        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use unwrap_or_else, which is lazily evaluated.

        :param default: default value.
        :return: The contained `Some` value or a provided default.
        """
        ...

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """
        :param f: Compute function in case option is `Empty`.
        :return: The contained `Some` value or computed value from the closure.
        """
        ...

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> "Option[U]":
        """
        Maps an `Option[T]` to `Option[U]` by applying a function to a contained value.
        :param f: Function to apply.
        :return: `Some(f(value))` if option is `Some(value)` else `Empty`
        """
        ...

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> "Option[U]":
        """
        Applies a function to the contained value (if any), or returns the provided default (if not).

        Arguments passed to map_or are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use map_or_else, which is lazily evaluated.

        :param default: default value
        :param f: function to apply
        :return: `Some(f(value))` if option is `Some(value)` else `default`
        """
        ...

    @abstractmethod
    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> "Option[U]":
        """
        Applies a function to the contained value (if any), or computes a default (if not).

        :param default: Default value.
        :param f: Function to apply to the map
        :return: `Some(f(value))` if option is `Some(value)` else `default()`
        """
        ...

    @abstractmethod
    def iter(self) -> Iterator[T]:
        """
        :return: An iterator over the contained value if option is `Some(T)` or an empty iterator if not.
        """
        ...

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        """
        :param predicate:
        :return: `Some(T)` if predicate returns `True` (where T is the wrapped value), `Empty` if predicate returns `False`
        """
        ...

    @abstractmethod
    def ok_or(self, err: E) -> "Result[T, E]":
        """
        Transforms the `Option[T]` into a `Result[T, E]`, mapping `Some(v)` to `Ok(v)` and `None` to `Err(err)`.

        Arguments passed to ok_or are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use ok_or_else, which is lazily evaluated.

        :param err: `Err` value
        :return: `Ok(T)` if option is `Some(T)` else `Err(err)`
        """
        ...

    @abstractmethod
    def ok_or_else(self, err: Callable[[], E]) -> "Result[T, E]":
        """
        Transforms the `Option[T]` into a `Result[T, E]`, mapping `Some(v)` to `Ok(v)` and `None` to `Err(err())`.
        :param err: Callable that return the `Err` value
        :return: `Ok(T)` if option is `Some(T)` else `Err(err())`
        """
        ...

    @abstractmethod
    def and_then(self, f: Callable[[T], "Option[T]"]) -> "Option[T]":
        """
        Some languages call this operation flatmap.

        :param f: The function to call.
        :return: `Empty` if the option is `Empty`, otherwise calls f with the wrapped value and returns the result.
        """
        ...

    @abstractmethod
    def or_else(self, f: Callable[[], "Option[T]"]) -> "Option[T]":
        """

        :param f: The function to call.
        :return: The option if it contains a value, otherwise calls f and returns the result.
        """
        ...

    @abstractmethod
    def xor(self, optb: "Option[T]") -> "Option[T]":
        """

        :param optb: `Option` to compare with.
        :return: `Some` if exactly one of self or optb is `Some`, otherwise returns `Empty`.
        """
        ...

    @abstractmethod
    def zip(self, value: "Option[U]") -> "Option[Tuple[T, U]]":
        """
        Zips self with another Option.
        :param value: `Option` to zip with.
        :return: If self is `Some[s]` and other is `Some[o]`, this method returns `Some[[s], [o]]`.
        Otherwise, `Empty` is returned.
        """
        ...

    @abstractmethod
    def zip_with(self, other: "Option[U]", f: Callable[[Tuple[T, U]], R]) -> "Option[R]":
        """
        Zips self and another Option with function f.

        :param other: `Option` to zip with.
        :param f: Function to apply to the zipped options values.
        :return: If self is `Some[s]` and other is `Some[o]`, this method returns `Some[f(s, o)]`.
        Otherwise, `Empty` is returned.
        """
        ...

    @abstractmethod
    def expect_empty(self, msg: str):
        """
        :param msg: Message to be wrapped by `UnwrapException` if raised
        :raises: `UnwrapException` if option is `Some`
        """
        ...

    @abstractmethod
    def unwrap_empty(self):
        """
        :raises: `UnwrapException` if option is `Some`
        """
        ...

    @abstractmethod
    def __bool__(self) -> bool:
        ...

    def __contains__(self, item: T) -> bool:
        return self.contains(item)

    def __iter__(self):
        return self.iter()


@dataclass(eq=True, frozen=True)
class Some(Generic[T]):
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

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return self.Value

    def map(self, f: Callable[[T], U]) -> "Option[U]":
        return Some(f(self.Value))

    def map_or(self, default: T, f: Callable[[T], T]) -> "Option[T]":
        return Some(f(self.Value))

    def map_or_else(self, default: Callable[[], T], f: Callable[[T], T]) -> "Option[T]":
        return Some(f(self.Value))

    def iter(self) -> Iterator[T]:
        def _iter():
            yield self.Value
        return iter(_iter())

    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        return self.copy() if predicate(self.Value) else Empty()

    def ok_or(self, err: E) -> "Result":
        return Ok(self.Value)

    def ok_or_else(self, f: Callable[[], E]) -> "Result":
        return Ok(self.Value)

    def and_then(self, f: Callable[[T], "Option[T]"]) -> "Option[T]":
        return f(self.Value)

    def or_else(self, f: Callable[[], "Option[T]"]) -> "Option[T]":
        return self.copy()

    def xor(self, optb: "Option[T]") -> "Option[T]":
        return self.copy() if optb.is_empty else Empty()

    def zip(self, other: "Option[U]") -> "Option[Tuple[T, U]]":
        if other.is_some:
            # function typing is correct, we really return an Option[Tuple] but mypy complains that
            # other may not have a Value attribute because it do not understand the previous line check.
            return Some((self.Value, other.Value))  # type: ignore

        return Empty()

    def zip_with(self, other: "Option[U]", f: Callable[[T, U], R]) -> "Option[R]":
        if other.is_some:
            # function typing is correct, we really return an Option[Tuple] but mypy complains that
            # other may not have a Value attribute because it do not understand the previous line check.
            return Some(f(self.Value, other.Value))  # type: ignore

        return Empty()

    def expect_empty(self, msg: str):
        raise UnwrapException(msg)

    def unwrap_empty(self):
        self.expect_empty("")

    def __bool__(self) -> bool:
        return True


@dataclass(eq=True, frozen=True)
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
        raise Exception(msg)

    def unwrap(self) -> T:
        raise UnwrapException("Tried to unwrap on an Empty value")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return f()

    def map(self, f: Callable[[T], U]) -> "Option[U]":
        return self

    def map_or(self, default: T, f: Callable[[T], T]) -> "Option[T]":
        return Some(default)

    def map_or_else(self, default: Callable[[], T], f: Callable[[T], T]) -> "Option[T]":
        return Some(default())

    def iter(self) -> Iterator[T]:
        return iter([])

    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        return self

    def ok_or(self, err: E) -> "Result":
        return Err(err)

    def ok_or_else(self, f: Callable[[], E]) -> "Result":
        return Err(f())

    def and_then(self, f: Callable[[T], "Option[T]"]) -> "Option[T]":
        return self

    def or_else(self, f: Callable[[], "Option[T]"]) -> "Option[T]":
        return f()

    def xor(self, optb: "Option[T]") -> "Option[T]":
        return optb if optb.is_some else Empty()

    def zip(self, value: "Option[U]") -> "Option[Tuple[T, U]]":
        return Empty()

    def zip_with(self, other: "Option[U]", f: Callable[[Tuple[T, U]], R]) -> "Option[R]":
        return Empty()

    def expect_empty(self, msg: str):
        ...

    def unwrap_empty(self):
        ...

    def __bool__(self) -> bool:
        return False


Option = Union[Some[T], Empty]


class ResultProtocol(Generic[T, E]):
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
    def map_err(self, f: Callable[[E], U]) -> "Result[T, U]":
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
class Ok(ResultProtocol[T, E]):
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

    def map(self, f: Callable[[T], U]) -> "Result[U, E]":
        return Ok(f(self.Value))

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self.Value)

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return f(self.Value)

    def map_err(self, f: Callable[[E], U]) -> "Result[T, U]":
        # Type ignored here. It complains that we do not transform error to U (E -> U)
        # since we do not really have an error, generic type remains the same.
        return self  # type: ignore

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
        # Type ignored here. It complains that we do not transform error to U (E -> U)
        # since we do not really have an error, generic type remains the same.
        return self  # type: ignore

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
class Err(ResultProtocol[T, E]):
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
        # Type ignored here. In this case U is the same type as T, but mypy cannot understand that match.
        return self  # type: ignore

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return default(self.Error)

    def map_err(self, f: Callable[[E], U]) -> "Result[T, U]":
        return Err(f(self.Error))

    def iter(self) -> Iterator[T]:
        return iter(tuple())

    def _and(self, res: "Result[T, E]") -> "Result[T, E]":
        return self and res

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        # Type ignored here. In this case U is the same type as T, but mypy cannot understand that match.
        return self  # type: ignore

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


Result = Union[Ok[T, E], Err[T, E]]