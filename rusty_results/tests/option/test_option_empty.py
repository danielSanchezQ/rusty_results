import pytest

from rusty_results.prelude import *


def test_empty_is_some():
    assert not Empty().is_some


def test_empty_is_empty():
    assert Empty().is_empty


def test_empty_contains():
    assert not Empty().contains(93)


def test_empty_expects():
    with pytest.raises(Exception):
        Empty().expects("")


def test_empty_unwrap():
    with pytest.raises(UnwrapException):
        Empty().unwrap()


def test_empty_unwrap_or():
    assert Empty().unwrap_or(30) == 30


def test_empty_unwrap_or_else():
    assert Empty().unwrap_or_else(lambda: 50) == 50


def test_empty_map():
    assert Empty().map(lambda x: 40) == Empty()


def test_empty_map_or():
    assert Empty().map_or(40, lambda x: x + 4) == 40


def test_empty_map_or_else():
    assert Empty().map_or_else(lambda: 40, lambda x: x+3) == 40


def test_empty_iter():
    assert list(Empty().iter()) == list(iter([]))


def test_empty_filter():
    assert Empty().filter(lambda x: True) == Empty()
    assert Empty().filter(lambda x: False) == Empty()


def test_empty_ok_or():
    assert Empty().ok_or(0) == Err(0)


def test_empty_ok_or_else():
    assert Empty().ok_or_else(lambda: 0) == Err(0)


def test_empty_and_then():
    assert Empty().and_then(lambda x: Some(4)) == Empty()
    assert Empty().and_then(lambda x: 0) == Empty()


def test_empty_or_else():
    assert Empty().or_else(lambda: Some(4)) == Some(4)


def test_empty_xor():
    assert Empty().xor(Some(5)) == Some(5)
    assert Empty().xor(Empty()) == Empty()


def test_empty_zip():
    assert Empty().zip(40) == Empty()


def test_empty_zip_with():
    assert Empty().zip_with(Some(4), lambda x, y: x + y) == Empty()


def test_empty_expect_none():
    Empty().expect_empty("")


def test_empty_unwrap_empty():
    Empty().unwrap_empty()
