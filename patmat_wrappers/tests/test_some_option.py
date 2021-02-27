from typing import Tuple

import pytest

from ..option import *


def create_some(value: int = 10) -> Tuple[Some[int], int]:
    return Some(value), value


def test_some_builds():
    some, value = create_some()
    assert some.Value == value


def test_some_is_some():
    some, value = create_some()
    assert some.is_some


def test_some_is_empty():
    some, value = create_some()
    assert not some.is_empty


def test_some_contains():
    some, value = create_some()
    assert some.contains(value)
    assert not some.contains(94)


def test_some_expects():
    some, value = create_some()
    assert some.expects("") == value
    assert some.expects("test") == value


def test_some_unwrap():
    some, value = create_some()
    assert some.unwrap() == value


def test_some_unwrap_or():
    some, value = create_some()
    assert some.unwrap_or(94) == value


def test_some_unwrap_or_else():
    some, value = create_some(0)
    assert some.unwrap_or_else(lambda x: 94) == value


def test_some_map():
    some, value = create_some()
    assert some.map(f=lambda x: x+5) == Some(value + 5)


def test_some_map_or():
    some, value = create_some()
    assert some.map_or(default=20, f=lambda x: x+5) == Some(value + 5)


def test_some_map_or_else():
    some, value = create_some()
    ret = some.map_or_else(default=lambda x: 94, f=lambda x: x+5)
    assert ret == Some(value + 5)
    assert ret.Value == value + 5


def test_some_iter():
    some, value = create_some()
    assert some.iter() == iter([10])


def test_some_filter():
    some, value = create_some()
    assert some.filter(predicate=lambda x: True) == some
    assert some.filter(predicate=lambda x: True).Value == value
    assert some.filter(predicate=lambda x: False) == Empty()


def test_some_and_then():
    some, value = create_some()
    assert some.and_then(lambda x: Some(x + 5)).Value == value + 5
    assert some.and_then(lambda x: Some(x + 5)) == Some(value + 5)


def test_some_or_else():
    some, value = create_some()
    assert some.or_else(f=lambda x: Some(x + 5)) == some


def test_some_xor():
    some, value = create_some()
    assert some.xor(optb=Empty()) == some
    assert some.xor(optb=Some(4)) == Empty()


def test_some_zip():
    some, value = create_some()
    assert some.zip(Empty()) == Empty()
    assert some.zip(Some(5)) == Some((value, 5))


def test_some_zip_with():
    some, value = create_some()
    assert some.zip_with(Empty(), lambda x, y: x + y) == Empty()
    assert some.zip_with(Some(5), lambda x, y: x + y) == Some(value + 5)


def test_some_expect_none():
    some, value = create_some()
    with pytest.raises(Exception):
        some.expect_none("")


def test_some_unwrap_empty():
    some, value = create_some()
    with pytest.raises(Exception):
        some.expect_none("")


def test_some_copy():
    some, value = create_some()
    assert some.copy() == some
    assert some.copy().Value == value


def test_option_and():
    assert (Some(5) and Some(10)) == Some(10)
    assert (Some(5) and Empty) == Empty
    assert (Empty and Empty) == Empty
    assert (Empty and Some(10)) == Empty


def test_option_or():
    assert (Some(5) and Some(10)) == Some(10)
    assert (Some(5) and Empty) == Some(5)
    assert (Empty and Empty) == Empty
    assert (Empty and Some(10)) == Some(10)
