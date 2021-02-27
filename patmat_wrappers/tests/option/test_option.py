from option import *


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


def test_option_hash():
    assert len({Some(0), Empty}) == 2
    assert len({Some(0), Some(1)}) == 2
    assert len({Empty, Empty}) == 2
    assert len({Some(0), Some(0)}) == 1
    assert len({Empty, Empty}) == 1
