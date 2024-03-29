from rusty_results import early_return, Option, Some, Empty


def test_early_return():
    @early_return
    def __test_it() -> Option[str]:
        foo: Option = Empty()
        _ = ~foo
        return Some(10)

    assert __test_it() == Empty()
