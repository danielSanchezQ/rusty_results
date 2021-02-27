import pytest

from option import *


def create_empty() -> Empty:
    return Empty()


def test_empty_builds():
    empty = create_empty()
    assert isinstance(empty, Empty)


def test_empty_is_some():
    empty = create_empty()
    assert not empty.is_some


def test_empty_is_empty():
    empty = create_empty()
    assert empty.is_empty


def test_empty_contains():
    empty = create_empty()
    assert not empty.contains(93)


def test_empty_expects():
    empty = create_empty()
    with pytest.raises(Exception):
        empty.expects("")


def test_empty_unwrap():
    empty = create_empty()
    with pytest.raises(Exception):
        empty.expects()


def test_empty_unwrap_or():
    empty = create_empty()
    assert empty.unwrap_or(30) == 30


def test_empty_unwrap_or_else():
    empty = create_empty()
    assert empty.unwrap_or_else(lambda: 50) == 50


def test_empty_map():
    empty = create_empty()
    assert empty.map(lambda x: 40) == empty


def test_empty_map_or():
    empty = create_empty()
    assert empty.map_or(40, lambda x: x + 4) == Some(40)


def test_empty_map_or_else():
    empty = create_empty()
    assert empty.map_or_else(lambda: 40, lambda x: x+3) == Some(40)


def test_empty_iter():
    empty = create_empty()
    assert empty.iter() == iter([])


def test_empty_filter():
    empty = create_empty()
    assert empty.filter(lambda x: True) == empty
    assert empty.filter(lambda x: False) == empty


def test_empty_and_then():
    empty = create_empty()
    assert empty.and_then(lambda x: Some(4)) == empty
    assert empty.and_then(lambda x: Empty()) == empty


def test_empty_or_else():
    empty = create_empty()
    assert empty.or_else(lambda: Some(4)) == Some(4)


def test_empty_xor():
    empty = create_empty()
    assert empty.xor(Some(5)) == Some(5)
    assert empty.xor(Empty()) == empty


def test_empty_zip():
    empty = create_empty()
    assert empty.zip(40) == Empty()


def test_empty_zip_with():
    empty = create_empty()
    assert empty.zip_with(Some(4), lambda x, y: x + y) == empty


def test_empty_expect_none():
    empty = create_empty()
    empty.expect_none("")


def test_empty_unwrap_empty():
    empty = create_empty()
    empty.unwrap_empty()
