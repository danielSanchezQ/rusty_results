from abc import abstractmethod
from dataclasses import dataclass
from typing import cast, TypeVar, Union, Callable, Generic, Iterator, Tuple, Dict, Any
from rusty_results.exceptions import UnwrapException
try:
    from pydantic.fields import ModelField
except ImportError:  # pragma: no cover
    ...

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
        ...  # pragma: no cover

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """
        :return: True if the option is `Empty`.
        """
        ...  # pragma: no cover

    @abstractmethod
    def contains(self, item: T) -> bool:
        """
        :param item: The value to check.
        :return: True if the option is `Some` containing the given value.
        """
        ...  # pragma: no cover

    @abstractmethod
    def expects(self, msg: str) -> T:
        """
        :param msg: Attached message for `UnwrapException` if raised.
        :return: The contained `Some` value
        :raises: `UnwrapException` if option is Empty.
        """
        ...  # pragma: no cover

    @abstractmethod
    def unwrap(self) -> T:
        """
        Because this function may panic, its use is generally discouraged.
        Instead, prefer to use pattern matching and handle the None case explicitly, or call unwrap_or, unwrap_or_else,
        or unwrap_or_default

        :return: The contained Some value, consuming the self value.
        :raises: `UnwrapException` if option is `Empty`
        """
        ...  # pragma: no cover

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """
        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use unwrap_or_else, which is lazily evaluated.

        :param default: default value.
        :return: The contained `Some` value or a provided default.
        """
        ...  # pragma: no cover

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """
        :param f: Compute function in case option is `Empty`.
        :return: The contained `Some` value or computed value from the closure.
        """
        ...  # pragma: no cover

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> "Option[U]":
        """
        Maps an `Option[T]` to `Option[U]` by applying a function to a contained value.
        :param f: Function to apply.
        :return: `Some(f(value))` if option is `Some(value)` else `Empty`
        """
        ...  # pragma: no cover

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """
        Applies a function to the contained value (if any), or returns the provided default (if not).

        Arguments passed to map_or are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use map_or_else, which is lazily evaluated.

        :param default: default value
        :param f: function to apply
        :return: f(value)` if option is `Some(value)` else `default`
        """
        ...  # pragma: no cover

    @abstractmethod
    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        """
        Applies a function to the contained value (if any), or computes a default (if not).

        :param default: Default value.
        :param f: Function to apply to the map
        :return: `Some(f(value))` if option is `Some(value)` else `default()`
        """
        ...  # pragma: no cover

    @abstractmethod
    def iter(self) -> Iterator[T]:
        """
        :return: An iterator over the contained value if option is `Some(T)` or an empty iterator if not.
        """
        ...  # pragma: no cover

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        """
        :param predicate:
        :return: `Some(T)` if predicate returns `True` (where T is the wrapped value), `Empty` if predicate returns `False`
        """
        ...  # pragma: no cover

    @abstractmethod
    def ok_or(self, err: E) -> "Result[T, E]":
        """
        Transforms the `Option[T]` into a `Result[T, E]`, mapping `Some(v)` to `Ok(v)` and `None` to `Err(err)`.

        Arguments passed to ok_or are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use ok_or_else, which is lazily evaluated.

        :param err: `Err` value
        :return: `Ok(T)` if option is `Some(T)` else `Err(err)`
        """
        ...  # pragma: no cover

    @abstractmethod
    def ok_or_else(self, err: Callable[[], E]) -> "Result[T, E]":
        """
        Transforms the `Option[T]` into a `Result[T, E]`, mapping `Some(v)` to `Ok(v)` and `None` to `Err(err())`.
        :param err: Callable that return the `Err` value
        :return: `Ok(T)` if option is `Some(T)` else `Err(err())`
        """
        ...  # pragma: no cover

    @abstractmethod
    def and_then(self, f: Callable[[T], "Option[T]"]) -> "Option[T]":
        """
        Some languages call this operation flatmap.

        :param f: The function to call.
        :return: `Empty` if the option is `Empty`, otherwise calls f with the wrapped value and returns the result.
        """
        ...  # pragma: no cover

    @abstractmethod
    def or_else(self, f: Callable[[], "Option[T]"]) -> "Option[T]":
        """

        :param f: The function to call.
        :return: The option if it contains a value, otherwise calls f and returns the result.
        """
        ...  # pragma: no cover

    @abstractmethod
    def xor(self, optb: "Option[T]") -> "Option[T]":
        """

        :param optb: `Option` to compare with.
        :return: `Some` if exactly one of self or optb is `Some`, otherwise returns `Empty`.
        """
        ...  # pragma: no cover

    @abstractmethod
    def zip(self, value: "Option[U]") -> "Option[Tuple[T, U]]":
        """
        Zips self with another Option.
        :param value: `Option` to zip with.
        :return: If self is `Some[s]` and other is `Some[o]`, this method returns `Some[[s], [o]]`.
        Otherwise, `Empty` is returned.
        """
        ...  # pragma: no cover

    @abstractmethod
    def zip_with(self, other: "Option[U]", f: Callable[[Tuple[T, U]], R]) -> "Option[R]":
        """
        Zips self and another Option with function f.

        :param other: `Option` to zip with.
        :param f: Function to apply to the zipped options values.
        :return: If self is `Some[s]` and other is `Some[o]`, this method returns `Some[f(s, o)]`.
        Otherwise, `Empty` is returned.
        """
        ...  # pragma: no cover

    @abstractmethod
    def expect_empty(self, msg: str):
        """
        :param msg: Message to be wrapped by `UnwrapException` if raised
        :raises: `UnwrapException` if option is `Some`
        """
        ...  # pragma: no cover

    @abstractmethod
    def unwrap_empty(self):
        """
        :raises: `UnwrapException` if option is `Some`
        """
        ...  # pragma: no cover

    @abstractmethod
    def flatten_one(self) -> "Option[T]":
        """
        Removes one level from a nested `Option` structure.
        E.g.:
        * `Some(Some(1))` becomes `Some(1)`.
        * `Some(Some(Some(1)))` becomes `Some(Some(1))`.
        :return: `Option[T]` if self is `Option[Option[T]]`, otherwise `self`
        """
        ...  # pragma: no cover

    @abstractmethod
    def flatten(self) -> "Option[T]":
        """
        Removes all levels of nesting from a nested `Option` structure.
        E.g.:
        * `Some(Some(1))` becomes `Some(1)`.
        * `Some(Some(Some(1)))` becomes `Some(1)`.
        * `Some(Some(Some(Empty())))` becomes `Empty()`.
        :return: `Option[T]` if self is `Option[ ... Option[T] ...]`, otherwise `self`
        """
        ...  # pragma: no cover

    @abstractmethod
    def transpose(self) -> "Result[Option[T], E]":
        """
        Transposes an Option of a Result into a Result of an Option.
        Empty will be mapped to Ok(Empty). Some(Ok(_)) and Some(Err(_)) will be mapped to Ok(Some(_)) and Err(_).
        :return: `Result[Option[T], E]`
        :raises TypeError if inner value is not a `Result`
        """
        ... # pragma: no cover

    @abstractmethod
    def __bool__(self) -> bool:
        ...  # pragma: no cover

    def __contains__(self, item: T) -> bool:
        return self.contains(item)

    def __iter__(self):
        return self.iter()

    @classmethod
    def __get_validators__(cls):
        yield cls.__validate

    @classmethod
    def __validate(cls, value: Union["Some", "Empty", Dict], field: "ModelField"):
        if isinstance(value, Some):
            return cls.__validate_some(value, field)
        elif isinstance(value, Empty):
            return cls.__validate_empty(value, field)
        elif isinstance(value, dict):
            return cls.__validate_dict(value, field)

        raise TypeError("Unable to validate Option")  # pragma: no cover

    @classmethod
    def __validate_some(cls, value: "Some", field: "ModelField"):
        import pydantic

        if not field.sub_fields:
            raise TypeError("No subfields found for Some")

        field_value = field.sub_fields[0]
        valid_value, error = field_value.validate(value.Some, {}, loc="")
        if error:
            # ignore type since it do not come from a base model
            raise pydantic.ValidationError((error, ), Some)  # type: ignore

        return Some(valid_value)

    @classmethod
    def __validate_empty(cls, _: "Empty", field: "ModelField"):
        if field.sub_fields:
            raise TypeError("Empty value cannot be bound to external types")

        return Empty()

    @classmethod
    def __validate_dict(cls, value: Dict, field: "ModelField"):
        import pydantic

        if value == {}:
            return Empty()

        if len(value) != 1:
            raise TypeError(
                "Extra object parameters found, Option can have strictly 0 (Empty) or 1 Value (Some)",
            )

        inner_value = value.get("Some")
        if inner_value is None:
            raise TypeError("Non Empty Option do not have a proper Value")

        if not field.sub_fields:
            raise TypeError("Cannot check Option pydantic subfields validations") # pragma: no cover

        field_value = field.sub_fields[0]
        valid_value, error = field_value.validate(value["Some"], {}, loc="")
        if error:
            # ignore type since it do not come from a base model
            raise pydantic.ValidationError(error, Option)  # type: ignore  # pragma: no cover

        return Some(valid_value)


@dataclass(eq=True, frozen=True)
class Some(OptionProtocol[T]):
    Some: T

    @property
    def is_some(self) -> bool:
        return True

    @property
    def is_empty(self) -> bool:
        return False

    def contains(self, item: T) -> bool:
        return item == self.Some

    def expects(self, msg: str) -> T:
        return self.Some

    def unwrap(self) -> T:
        return self.Some

    def unwrap_or(self, default: T) -> T:
        return self.Some

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return self.Some

    def map(self, f: Callable[[T], U]) -> "Option[U]":
        return Some(f(self.Some))

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self.Some)

    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        return f(self.Some)

    def iter(self) -> Iterator[T]:
        def _iter():
            yield self.Some
        return iter(_iter())

    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        return self if predicate(self.Some) else Empty()

    def ok_or(self, err: E) -> "Result[T, E]":
        return Ok(self.Some)

    def ok_or_else(self, err: Callable[[], E]) -> "Result[T, E]":
        return Ok(self.Some)

    def and_then(self, f: Callable[[T], "Option[T]"]) -> "Option[T]":
        return f(self.Some)

    def or_else(self, f: Callable[[], "Option[T]"]) -> "Option[T]":
        return self

    def xor(self, optb: "Option[T]") -> "Option[T]":
        return self if optb.is_empty else Empty()

    def zip(self, other: "Option[U]") -> "Option[Tuple[T, U]]":
        if other.is_some:
            # function typing is correct, we really return an Option[Tuple] but mypy complains that
            # other may not have a Value attribute because it do not understand the previous line check.
            return Some((self.Some, other.Some))  # type: ignore[union-attr]

        return Empty()

    def zip_with(self, other: "Option[U]", f: Callable[[Tuple[T, U]], R]) -> "Option[R]":
        return self.zip(other).map(f)

    def expect_empty(self, msg: str):
        raise UnwrapException(msg)

    def unwrap_empty(self):
        self.expect_empty("")

    def flatten_one(self) -> "Option[T]":
        inner: T = self.unwrap()
        if isinstance(inner, OptionProtocol):
            return cast(Option, inner)
        return self

    def flatten(self) -> "Option[T]":
        this: Option[T] = self
        inner: Option[T] = self.flatten_one()
        while inner is not this:
            this, inner = (inner, inner.flatten_one())
        return this

    def transpose(self) -> "Result[Option[T], E]":
        if not isinstance(self.Some, ResultProtocol):
            raise TypeError("Inner value is not a Result")
        value: "ResultProtocol[T, E]" = self.Some
        return value.map(Some)

    def __bool__(self) -> bool:
        return True

    @classmethod
    def __get_validators__(cls):
        yield from OptionProtocol.__get_validators__()


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
        raise UnwrapException(msg)

    def unwrap(self) -> T:
        raise UnwrapException("Tried to unwrap on an Empty value")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return f()

    def map(self, f: Callable[[T], U]) -> "Option[U]":
        return self

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        return default()

    def iter(self) -> Iterator[T]:
        return iter([])

    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        return self

    def ok_or(self, err: E) -> "Result[T, E]":
        return Err(err)

    def ok_or_else(self, err: Callable[[], E]) -> "Result[T, E]":
        return Err(err())

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

    def flatten_one(self) -> "Option[T]":
        return self

    def flatten(self) -> "Option[T]":
        return self

    def transpose(self) -> "Result[Option[T], E]":
        return Ok(self)

    def __bool__(self) -> bool:
        return False

    @classmethod
    def __get_validators__(cls):
        yield from OptionProtocol.__get_validators__()


Option = Union[Some[T], Empty]


class ResultProtocol(Generic[T, E]):
    @property
    @abstractmethod
    def is_ok(self) -> bool:
        """
        :return: True if the result is Ok
        """
        ...  # pragma: no cover

    @property
    @abstractmethod
    def is_err(self) -> bool:
        """
        :return: True if the result is Err
        """
        ...  # pragma: no cover

    @abstractmethod
    def contains(self, value: T) -> bool:
        """
        :param value: Value to be checked
        :return: True if the result is an Ok value containing the given value
        """
        ...  # pragma: no cover

    @abstractmethod
    def contains_err(self, err: E) -> bool:
        """
        :param err: Value to be checked
        :return: True if the result is an Err containing the given err value
        """
        ...  # pragma: no cover

    @abstractmethod
    def ok(self) -> Option[T]:
        """
        Converts from `Result[T, E]` to `Option[T]`
        :return: `Some(T)` if result is `Ok(T)` otherwise `Empty` discarding the error, if any.
        """
        ...  # pragma: no cover

    @abstractmethod
    def err(self) -> Option[E]:
        """
        Converts from `Result[T, E]` to `Option[E]`
        :return: `Some(E)` if result is `Err(E)` otherwise `Empty` discarding the success value, if any.
        """
        ...  # pragma: no cover

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> "Result[U, E]":
        """
        Maps a `Result[T, E]` to `Result[U, E]` by applying a function to a contained Ok value, leaving an Err value untouched.

        This function can be used to compose the results of two functions.
        :param f: Function to apply to the `Ok(T)`
        :return: A new result wrapping the new value, if applied.
        """
        ...  # pragma: no cover

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """
        Applies a function to the contained value (if Ok), or returns the provided default (if Err).

        Arguments passed to map_or are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use map_or_else, which is lazily evaluated.
        :param default: Default value to be returned if result ir Err
        :param f: Function to apply to the `Ok(T)`
        :return: A new value with the result of applying the function to the Ok(value) or the default value.
        """
        ...  # pragma: no cover

    @abstractmethod
    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        """
        Maps a `Result[T, E]` to `U` by applying a function to a contained Ok value,
        or a fallback function to a contained Err value.

        This function can be used to unpack a successful result while handling an error.
        :param default: Callable to lazy load the default return value
        :param f: Function to apply to the `Ok(T)`
        :return: A new value with the result of applying the function to the Ok(value) or the default value loaded from the default function call.
        """
        ...  # pragma: no cover

    @abstractmethod
    def map_err(self, f: Callable[[E], U]) -> "Result[T, U]":
        """
        Maps a `Result[T, E]` to `Result[T, F]` by applying a function to a contained `Err` value,
        leaving an Ok value untouched.

        This function can be used to pass through a successful result while handling an error.
        :param f: Function to apply to the `E`
        :return: A new result with the modified `Err` value if applies.
        """
        ...  # pragma: no cover

    @abstractmethod
    def iter(self) -> Iterator[T]:
        """
        :return: An iterator with a value if the result is `Ok` otherwise an empty iterator.
        """
        ...  # pragma: no cover

    @abstractmethod
    def and_then(self, op: Callable[[T], "Result[T, E]"]) -> "Result[T, E]":
        """
        Calls op if the result is `Ok`, otherwise returns the `Err` value of self.

        This function can be used for control flow based on Result values.
        :param op: Callable to apply if result value if is `Ok`
        :return: A result from applying op if `Ok`, original `Err` if not
        """
        ...  # pragma: no cover

    @abstractmethod
    def or_else(self, op: Callable[[E], U]) -> "Result[T, U]":
        """
        Calls op if the result is `Err`, otherwise returns the `Ok` value of self.

        This function can be used for control flow based on Result values.
        :param op: Callable to apply if result value if is `Err`
        :return: A result from applying op if `Err`, original `Ok` if not
        """
        ...  # pragma: no cover

    @abstractmethod
    def unwrap(self) -> T:
        """
        Returns the contained `Ok` value.

        Because this function may raise an exception, its use is generally discouraged. Instead, prefer to use
        pattern matching and handle the `Err` case explicitly, or call unwrap_or, unwrap_or_else, or unwrap_or_default.
        :return: Contained `Ok` value
        :raises: `UnwrapException` if resutl is `Err`
        """
        ...  # pragma: no cover

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """
        Returns the contained `Ok` value or a provided default.

        Arguments passed to unwrap_or are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use unwrap_or_else, which is lazily evaluated.
        :param default: Value to be returned if result is `Err`
        :return: `Ok` value or `default`
        """
        ...  # pragma: no cover

    @abstractmethod
    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        """
        :param default: Function to call for the default value
        :return: The contained `Ok` value or computes it from a closure.
        """
        ...  # pragma: no cover

    @abstractmethod
    def expect(self, msg: str) -> T:
        """
        :param msg: Attached message in case result is `Err` and `UnwrapException` is raised
        :return: The contained `Ok` value
        :raises: `UnwrapException`
        """
        ...  # pragma: no cover

    @abstractmethod
    def unwrap_err(self) -> E:
        """
        :return: The contained `Err` value.
        :raises: `UnwrapException` if result is `Ok`.
        """
        ...  # pragma: no cover

    @abstractmethod
    def expect_err(self, msg: str) -> E:
        """
        :param msg: Attached message in case result is `Ok` and `UnwrapException` is raised
        :return: The contained `Err` value.
        :raises: `UnwrapException` if result is `Ok`.
        """
        ...  # pragma: no cover

    @abstractmethod
    def flatten_one(self) -> "Result[T, E]":
        """
        Converts from Result[Result[T, E], E] to Result<T, E>, one nested level.
        :return: Flattened Result[T, E]
        """
        ... # pragma: no cover

    @abstractmethod
    def flatten(self) -> "Result[T, E]":
        """
        Converts from Result[Result[T, E], E] to Result<T, E>, any nested level
        :return: Flattened Result[T, E]
        """
        ... # pragma: no cover

    @abstractmethod
    def transpose(self) -> Option["Result[T, E]"]:
        """
        Transposes a Result of an Option into an Option of a Result.
        Ok(Empty) will be mapped to Empty. Ok(Some(_)) and Err(_) will be mapped to Some(Ok(_)) and Some(Err(_))
        :return: Option[Result[T, E]] as per the mapping above
        :raises TypeError if inner value is not an `Option`
        """
        ... # pragma: no cover

    @abstractmethod
    def __bool__(self) -> bool:
        ...  # pragma: no cover

    def __contains__(self, item: T) -> bool:
        return self.contains(item)

    def __iter__(self) -> Iterator[T]:
        return self.iter()

    @classmethod
    def __get_validators__(cls):
        yield cls.__validate

    @classmethod
    def __validate(cls, value: Union["Ok", "Err", Dict], field: "ModelField"):
        if isinstance(value, Ok):
            return cls.__validate_ok(value, field)
        elif isinstance(value, Err):
            return cls.__validate_err(value, field)
        elif isinstance(value, dict):
            return cls.__validate_dict(value, field)

        raise TypeError("Unable to validate Result")  # pragma: no cover

    @classmethod
    def __validate_ok(cls, value: "Ok", field: "ModelField"):
        import pydantic

        if not field.sub_fields or len(field.sub_fields) != 2:
            raise TypeError("Wrong subfields found for Ok") # pragma: no cover

        field_value = field.sub_fields[0]
        valid_value, error = field_value.validate(value.Ok, {}, loc="")
        if error:
            # ignore type since it do not come from a base model
            raise pydantic.ValidationError(error, Result)  # type: ignore

        return Ok(valid_value)

    @classmethod
    def __validate_err(cls, value: "Err", field: "ModelField"):
        import pydantic

        if not field.sub_fields or len(field.sub_fields) != 2:
            raise TypeError("Wrong subfields found for Ok") # pragma: no cover

        field_value = field.sub_fields[1]
        valid_value, error = field_value.validate(value.Error, {}, loc="")
        if error:
            # ignore type since it do not come from a base model
            raise pydantic.ValidationError(error, Result)  # type: ignore

        return Err(valid_value)

    @classmethod
    def __validate_dict(cls, value: Dict, field: "ModelField"):  # mypy: ignore
        import pydantic

        if not field.sub_fields or len(field.sub_fields) != 2:
            raise TypeError("Wrong subfields found for Ok") # pragma: no cover

        if len(value) != 1:
            raise TypeError(
                "Extra object parameters found, Results have strictly 1 value (either Value (Ok) or Error (Err))"
            )  # pragma: no cover

        return_class: Callable[[Any], Any]
        inner_value: Any
        if "Ok" in value:
            inner_value, return_class, subfield = value.get("Ok"), Ok, 0
        elif "Error" in value:
            inner_value, return_class, subfield = value.get("Error"), Err, 1
        else:
            # should never be able to reach here
            raise TypeError("Cannot find any Result correct value")  # pragma: no cover

        field_value = field.sub_fields[subfield]
        valid_value, error = field_value.validate(inner_value, {}, loc="")
        if error:
            # ignore type since it do not come from a base model
            raise pydantic.ValidationError(error, Result)  # type: ignore  # pragma: no cover

        return return_class(valid_value)


@dataclass(eq=True, frozen=True)
class Ok(ResultProtocol[T, E]):
    Ok: T

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False

    def contains(self, value: T) -> bool:
        return self.Ok == value

    def contains_err(self, err: E) -> bool:
        return False

    def ok(self) -> Option[T]:
        return Some(self.Ok)

    def err(self) -> Option[E]:
        return Empty()

    def map(self, f: Callable[[T], U]) -> "Result[U, E]":
        return Ok(f(self.Ok))

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self.Ok)

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return f(self.Ok)

    def map_err(self, f: Callable[[E], U]) -> "Result[T, U]":
        # Type ignored here. It complains that we do not transform error to U (E -> U)
        # since we do not really have an error, generic type remains the same.
        return self  # type: ignore

    def iter(self) -> Iterator[T]:
        def _iter():
            yield self.Ok
        return iter(_iter())

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return op(self.Ok)

    def or_else(self, op: Callable[[E], U]) -> "Result[T, U]":
        # Type ignored here. It complains that we do not transform error to U (E -> U)
        # since we do not really have an error, generic type remains the same.
        return self  # type: ignore

    def unwrap(self) -> T:
        return self.Ok

    def unwrap_or(self, default: T) -> T:
        return self.Ok

    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        return self.Ok

    def expect(self, msg: str) -> T:
        return self.Ok

    def unwrap_err(self) -> E:
        raise UnwrapException(f"{self.Ok}")

    def expect_err(self, msg: str) -> E:
        raise UnwrapException(msg)

    def flatten_one(self) -> "Result[T, E]":
        if isinstance(self.Ok, ResultProtocol):
            return cast(Result, self.unwrap())
        return self

    def flatten(self) -> "Result[T, E]":
        this: Result[T, E] = self
        inner: Result[T, E] = self.flatten_one()
        while inner is not this:
            this, inner = (inner, inner.flatten_one())
        return this

    def transpose(self) -> Option["Result[T, E]"]:
        if not isinstance(self.Ok, OptionProtocol):
            raise TypeError("Inner value is not of type Option")
        return cast(Option, self.unwrap()).map(Ok)

    def __repr__(self):
        return f"Ok({self.Ok})"

    def __bool__(self):
        return True

    @classmethod
    def __get_validators__(cls):
        yield from ResultProtocol.__get_validators__()


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

    def and_then(self, op: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        # Type ignored here. In this case U is the same type as T, but mypy cannot understand that match.
        return self  # type: ignore

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

    def flatten_one(self) -> "Result[T, E]":
        return self

    def flatten(self) -> "Result[T, E]":
        return self

    def transpose(self) -> Option["Result[T, E]"]:
        return Some(self)

    def __repr__(self):
        return f"Err({self.Error})"

    def __bool__(self):
        return False

    @classmethod
    def __get_validators__(cls):
        yield from ResultProtocol.__get_validators__()


Result = Union[Ok[T, E], Err[T, E]]