import pytest
from rusty_results.prelude import *


def test_ok_builds():
    value: int = 10
    ok: Result[int, str] = Ok(value)
    assert ok.Ok == value
    assert ok.is_ok
    assert not ok.is_err


def test_ok_repr():
    assert Ok(0) == eval(repr(Ok(0)))


def test_ok_contains():
    ok: Result[int, int] = Ok(0)
    assert ok.contains(0)
    assert not ok.contains_err(0)


def test_ok_ok():
    ok: Result[int, int] = Ok(0)
    assert ok.ok() == Some(0)


def test_ok_err():
    ok: Result[int, int] = Ok(0)
    assert ok.err() == Empty()


def test_ok_map():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    ok: Result[int, int] = Ok(0)

    assert ok.map(function) == Ok(10)
    assert ok.map(lambda_function) == Ok(100)


def test_ok_map_or():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    ok: Result[int, int] = Ok(0)

    assert ok.map_or(1, function) == 10
    assert ok.map_or(1, lambda_function) == 100


def test_ok_map_or_else():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    ok: Result[int, int] = Ok(0)

    assert ok.map_or_else(lambda_function, function) == 10
    assert ok.map_or_else(function, lambda_function) == 100


def test_ok_map_err():
    @pytest.mark.no_cover
    def function(i: int) -> int:
        return i + 10  # pragma: no cover

    lambda_function: Callable[[int], int] = lambda x: x+100

    ok: Result[int, int] = Ok(0)

    assert ok.map_err(function) == ok
    assert ok.map_err(lambda_function) == ok


def test_ok_iter():
    ok: Result[int, int] = Ok(0)
    assert list(ok) == [0]


def test_ok_and_then():
    ok: Result[int, int] = Ok(0)

    def op(x: int) -> Result[int, int]:
        return Ok(x+10)

    assert ok.and_then(op) == Ok(10)


def test_ok_or_else():
    ok: Result[int, int] = Ok(0)

    @pytest.mark.no_cover
    def op(e: int) -> int:
        return e+10  # pragma: no cover

    assert ok.or_else(op) == ok


def test_ok_unwrap():
    ok: Result[int, int] = Ok(0)
    assert ok.unwrap() == 0


def test_ok_unwrap_or():
    ok: Result[int, int] = Ok(0)
    assert ok.unwrap_or(1) == 0


def test_ok_unwrap_or_else():
    ok: Result[int, int] = Ok(0)
    assert ok.unwrap_or_else(lambda: 1) == 0


def test_ok_expect():
    ok: Result[int, int] = Ok(0)
    assert ok.expect("foo") == 0


def test_ok_unwrap_err():
    ok: Result[int, int] = Ok(0)
    with pytest.raises(UnwrapException):
        ok.unwrap_err()


def test_ok_expect_err():
    exception_msg = "foo"
    ok: Result[int, int] = Ok(0)
    with pytest.raises(UnwrapException) as e:
        ok.expect_err(exception_msg)
    assert str(e.value) == exception_msg
