import pytest
from patmat_wrappers.result import *


def test_ok_builds():
    value: int = 10
    ok: Result[int, str] = Ok(value)
    assert ok.Value == value
    assert ok.is_ok
    assert not ok.is_err


def test_err_builds():
    msg: str = "Bang!"
    err:  Result[int, str] = Err(msg)
    assert err.Error == msg
    assert err.is_err
    assert not err.is_ok


def test_result_eq():
    assert Ok(0) == Ok(0)
    assert Err(0) == Err(0)
    assert Ok(0) != Ok(1)
    assert Err(0) != Err(1)
    assert Ok(0) != Err(0)
    assert Ok("0") != Ok(0)
    assert Ok(0) != 0


def test_ok_repr():
    assert Ok(0) == eval(repr(Ok(0)))


def test_err_repr():
    assert Err(0) == eval(repr(Err(0)))


def test_result_hash():
    assert len({Ok(0), Err(0)}) == 2
    assert len({Ok(0), Ok(1)}) == 2
    assert len({Err(0), Err(1)}) == 2
    assert len({Ok(0), Ok(0)}) == 1
    assert len({Err(0), Err(0)}) == 1


def test_ok_contains():
    ok: Result[int, int] = Ok(0)
    assert ok.contains(0)
    assert not ok.contains_err(0)


def test_err_contains():
    err: Result[int, int] = Err(0)
    assert not err.contains(0)
    assert err.contains_err(0)


def test_ok_ok():
    # TODO: implement when Option is finished
    ok: Result[int, int] = Ok(0)


def test_err_ok():
    # TODO: implement when Option is finished
    err: Result[int, int] = Err(0)


def test_ok_err():
    # TODO: implement when Option is finished
    ok: Result[int, int] = Ok(0)


def test_err_err():
    # TODO: implement when Option is finished
    err: Result[int, int] = Err(0)


def test_ok_map():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    ok: Result[int, int] = Ok(0)

    assert ok.map(function) == Ok(10)
    assert ok.map(lambda_function) == Ok(100)


def test_err_map():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    err: Result[int, int] = Err(0)

    assert err.map(function) == err
    assert err.map(lambda_function) == err


def test_ok_map_or():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    ok: Result[int, int] = Ok(0)

    assert ok.map_or(1, function) == 10
    assert ok.map_or(1, lambda_function) == 100


def test_err_map_or():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    err: Result[int, int] = Err(0)

    assert err.map_or(1, function) == 1
    assert err.map_or(1, lambda_function) == 1


def test_ok_map_or_else():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    ok: Result[int, int] = Ok(0)

    assert ok.map_or_else(lambda_function, function) == 10
    assert ok.map_or_else(function, lambda_function) == 100


def test_err_map_or_else():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    err: Result[int, int] = Err(0)

    assert err.map_or_else(function, lambda_function) == 10
    assert err.map_or_else(lambda_function, function) == 100


def test_ok_map_err():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    ok: Result[int, int] = Ok(0)

    assert ok.map_err(function) == ok
    assert ok.map_err(lambda_function) == ok


def test_err_map_err():
    def function(i: int) -> int:
        return i + 10

    lambda_function: Callable[[int], int] = lambda x: x+100

    err: Result[int, int] = Err(0)

    assert err.map_err(function) == Err(10)
    assert err.map_err(lambda_function) == Err(100)


def test_ok_iter():
    ok: Result[int, int] = Ok(0)
    assert list(ok) == [0]


def test_err_iter():
    err: Result[int, int] = Err(0)
    assert list(err) == []


def test_result_and():
    assert (Ok(0) and Ok(1)) == Ok(1)
    assert (Ok(0) and Err(0)) == Err(0)
    assert (Err(0) and Err(1)) == Err(0)
    assert (Err(0) and Ok(1)) == Err(0)


def test_ok_and_then():
    ok: Result[int, int] = Ok(0)

    def op(x: int) -> Result[int, int]:
        return Ok(x+10)

    assert ok.and_then(op) == Ok(10)


def test_err_and_then():
    err: Result[int, int] = Err(0)

    def op(x: int) -> Result[int, int]:
        return Ok(x+10)

    assert err.and_then(op) == err


def test_result_or():
    assert (Ok(0) or Ok(1)) == Ok(0)
    assert (Ok(0) or Err(0)) == Ok(0)
    assert (Err(0) or Err(1)) == Err(1)
    assert (Err(0) or Ok(1)) == Ok(1)


def test_ok_or_else():
    ok: Result[int, int] = Ok(0)

    def op(e: int) -> int:
        return e+10

    assert ok.or_else(op) == ok


def test_err_or_else():
    err: Result[int, int] = Err(0)

    def op(e: int) -> int:
        return e+10

    assert err.or_else(op) == Err(10)


def test_ok_unwrap():
    ok: Result[int, int] = Ok(0)
    assert ok.unwrap() == 0


def test_err_unwrap():
    err: Result[int, int] = Err(0)
    with pytest.raises(UnwrapException):
        err.unwrap()


def test_ok_unwrap_or():
    ok: Result[int, int] = Ok(0)
    assert ok.unwrap_or(1) == 0


def test_err_unwrap_or():
    err: Result[int, int] = Err(0)
    assert err.unwrap_or(1) == 1


def test_ok_unwrap_or_else():
    ok: Result[int, int] = Ok(0)
    assert ok.unwrap_or_else(lambda: 1) == 0


def test_err_unwrap_or_else():
    err: Result[int, int] = Err(0)
    assert err.unwrap_or_else(lambda: 1) == 1


def test_ok_expect():
    ok: Result[int, int] = Ok(0)
    assert ok.expect("foo") == 0


def test_err_expect():
    exception_msg = "foo"
    err: Result[int, int] = Err(0)
    with pytest.raises(UnwrapException) as e:
        err.expect(exception_msg)
    assert str(e.value) == exception_msg


def test_ok_unwrap_err():
    ok: Result[int, int] = Ok(0)
    with pytest.raises(UnwrapException):
        ok.unwrap_err()


def test_err_unwrap_err():
    err: Result[int, int] = Err(0)
    assert err.unwrap_err() == 0


def test_ok_expect_err():
    exception_msg = "foo"
    ok: Result[int, int] = Ok(0)
    with pytest.raises(UnwrapException) as e:
        ok.expect_err(exception_msg)
    assert str(e.value) == exception_msg


def test_err_expect_err():
    err: Result[int, int] = Err(0)
    assert err.expect_err("foo") == 0
