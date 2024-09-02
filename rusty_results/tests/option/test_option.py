from rusty_results.prelude import *


def test_option_and():
    assert (Some(5) and Some(10)) == Some(10)
    assert (Some(5) and Empty()) == Empty()
    assert (Empty() and Empty()) == Empty()
    assert (Empty() and Some(10)) == Empty()


def test_option_or():
    assert (Some(5) or Some(10)) == Some(5)
    assert (Some(5) or Empty()) == Some(5)
    assert (Empty() or Empty()) == Empty()
    assert (Empty() or Some(10)) == Some(10)


def test_option_hash():
    assert len({Some(0), Empty()}) == 2
    assert len({Some(0), Some(1)}) == 2
    assert len({Empty(), Empty()}) == 1
    assert len({Some(0), Some(0)}) == 1
    assert len({Empty(), Empty()}) == 1


def test_option_contains():
    assert 0 in Some(0)
    assert 0 not in Empty()
    assert 1 not in Some(0)


def test_option_iter():
    assert list(iter(Empty())) == []
    assert list(iter(Some(1))) == [1]


def test_option_from():
    assert Some(0) == option_from(0)
    assert Empty() == option_from(None)
    example_dictionary = {"data": 5}
    assert Empty() == option_from(example_dictionary.get("key_not_found"))
    assert Some(5) == option_from(example_dictionary.get("data"))
    opt = Some(3)
    assert opt == option_from(opt)
    assert Empty() == option_from(Empty())
    nested_opt = Some(Some(Some(Some(3))))
    assert nested_opt == option_from(nested_opt)
