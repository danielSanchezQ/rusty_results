import pytest
from rusty_results.prelude import *


def test_result_eq():
    assert Ok(0) == Ok(0)
    assert Err(0) == Err(0)
    assert Ok(0) != Ok(1)
    assert Err(0) != Err(1)
    assert Ok(0) != Err(0)
    assert Ok("0") != Ok(0)
    assert Ok(0) != 0


def test_result_hash():
    assert len({Ok(0), Err(0)}) == 2
    assert len({Ok(0), Ok(1)}) == 2
    assert len({Err(0), Err(1)}) == 2
    assert len({Ok(0), Ok(0)}) == 1
    assert len({Err(0), Err(0)}) == 1


def test_result_and():
    assert (Ok(0) and Ok(1)) == Ok(1)
    assert (Ok(0) and Err(0)) == Err(0)
    assert (Err(0) and Err(1)) == Err(0)
    assert (Err(0) and Ok(1)) == Err(0)


def test_result_or():
    assert (Ok(0) or Ok(1)) == Ok(0)
    assert (Ok(0) or Err(0)) == Ok(0)
    assert (Err(0) or Err(1)) == Err(1)
    assert (Err(0) or Ok(1)) == Ok(1)


def test_result_contains():
    assert 0 in Ok(0)
    assert 1 not in Ok(0)
    assert 1 not in Err(0)
    assert 0 not in Err(0)
