import pytest
from rusty_results.prelude import *


def test_err_builds():
    msg: str = "Bang!"
    err:  Result[int, str] = Err(msg)
    assert err.Error == msg
    assert err.is_err
    assert not err.is_ok


def test_err_repr():
    assert Err(0) == eval(repr(Err(0)))


def test_err_contains():
    err: Result[int, int] = Err(0)
    assert not err.contains(0)
    assert err.contains_err(0)


def test_err_ok():
    err: Result[int, int] = Err(0)
    assert err.ok() == Empty()


def test_err_err():
    err: Result[int, int] = Err(0)
    assert err.err() == Some(0)


def test_err_map():
    def function(i: int) -> int:
        return i + 10  # pragma: no cover

    lambda_function: Callable[[int], int] = lambda x: x+100

    err: Result[int, int] = Err(0)

    assert err.map(function) == err
    assert err.map(lambda_function) == err


def test_err_map_or():
    def function(i: int) -> int:
        return i + 10  # pragma: no cover

    lambda_function: Callable[[int], int] = lambda x: x+100

    err: Result[int, int] = Err(0)

    assert err.map_or(1, function) == 1
    assert err.map_or(1, lambda_function) == 1


def test_err_map_or_else():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    err: Result[int, int] = Err(0)

    assert err.map_or_else(function, lambda_function) == 10
    assert err.map_or_else(lambda_function, function) == 100


def test_err_map_err():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    err: Result[int, int] = Err(0)

    assert err.map_err(function) == Err(10)
    assert err.map_err(lambda_function) == Err(100)


def test_err_iter():
    err: Result[int, int] = Err(0)
    assert list(err) == []


def test_err_and_then():
    err: Result[int, int] = Err(0)

    def op(x: int) -> Result[int, int]:
        return Ok(x+10)  # pragma: no cover

    assert err.and_then(op) == err


def test_err_or_else():
    err: Result[int, int] = Err(0)

    def op(e: int) -> int:
        return e+10

    assert err.or_else(op) == Err(10)


def test_err_unwrap():
    err: Result[int, int] = Err(0)
    with pytest.raises(UnwrapException):
        err.unwrap()


def test_err_unwrap_or():
    err: Result[int, int] = Err(0)
    assert err.unwrap_or(1) == 1


def test_err_unwrap_or_else():
    err: Result[int, int] = Err(0)
    assert err.unwrap_or_else(lambda: 1) == 1


def test_err_expect():
    exception_msg = "foo"
    err: Result[int, int] = Err(0)
    with pytest.raises(UnwrapException) as e:
        err.expect(exception_msg)
    assert str(e.value) == exception_msg


def test_err_unwrap_err():
    err: Result[int, int] = Err(0)
    assert err.unwrap_err() == 0


def test_err_expect_err():
    err: Result[int, int] = Err(0)
    assert err.expect_err("foo") == 0
