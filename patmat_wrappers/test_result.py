import pytest
from .result import *


def test_ok_builds():
    value: int = 10
    ok: Result[int, str] = Ok(value)
    assert ok.Value == value


def test_err_builds():
    msg: str = "Bang!"
    err:  Result[int, str] = Err(msg)
    assert err.Error == msg




